import urllib.parse

from PySense import PySenseDataModel, PySenseException, PySenseGroup, PySenseRule, PySenseUser, PySenseUtils, \
    SisenseVersion


class Elasticube:
    """An Elasticube

    If in Linux, more functionality is available from the data model.

    Attributes:
        json (JSON): The JSON for this object
        py_client (PySense): The connection to the Sisense server which owns this asset
        server_address (str): The server address of the server this elasticube belongs to.
    """

    def __init__(self, py_client, elasticube_json):
        """
        Server address is set to 'localhost' by default.
        If available, we will try to set the server address from the metadata.
        If using an elasticube set on windows, server address is set to 'Set'.
        After object creation, feel free to set the server_address manually.

        Args:
            py_client (PySense): The PySense object for the server this asset belongs to
            elasticube_json (JSON): The json for this object
        """

        self.json = elasticube_json
        self.py_client = py_client
        self.server_address = 'localhost'
        if py_client.version == SisenseVersion.Version.WINDOWS:
            metadata = self.get_metadata()
            if metadata is None:
                print('No meta data for cube {}'.format(self.get_title()))
            elif 'address' in metadata:
                self.server_address = metadata['address']
            elif metadata['fullname'].endswith(' - Set'):
                self.server_address = 'Set'

    def get_oid(self):
        """Returns the Elasticube id"""

        if 'oid' in self.json:
            return self.json['oid']
        else:
            raise PySenseException('Cube {} is not currently running so this action cannot be performed')

    def get_model(self):
        """Returns the data model object for the cube.

        Linux only

        Returns:
            DataModel: The data model for the cube
        """

        PySenseUtils.validate_version(self.py_client, SisenseVersion.Version.LINUX, 'get_model')

        query_params = {'datamodelId': self.get_oid(), 'type': 'schema-latest'}

        data_model_json = self.py_client.connector.rest_call(
            'get', 'api/v2/datamodel-exports/schema', query_params=query_params)

        data_model_json['oid'] = self.get_oid()

        return PySenseDataModel.DataModel(self.py_client, data_model_json)

    def get_title(self, url_encoded=False):
        """Returns the Elasticube's title.

        Args:
           url_encoded (bool): (Optional) True to url encode the name. Useful for passing as query parameter.

        Returns:
             str: The name of the Elasticube, url encoded if set.
        """

        if url_encoded:
            return urllib.parse.quote(self.json['title'])
        else:
            return self.json['title']

    def run_sql(self, query, file_type, path, *,
                offset=None, count=None, include_metadata=None, is_masked_response=None):
        """Executes SQL against ElastiCube and prints results to file

        Args:
            query (str): The query to execute
            file_type (str): File format to return (csv)
            path (str): The location to save the file
            offset (num): (Optional) Defines how many items to skip before returning the results.
                For example, to return results from value #101 onward, enter a value of ‘100’.
            count (num): (Optional) Limits the result set to a defined number of results.
                Enter 0 (zero) or leave blank not to limit.
            include_metadata (bool): (Optional) Whether to include metadata.
            is_masked_response (bool): (Optional) Whether response should be masked.

        Returns:
             str: The path of the created file
        """

        query = query.replace(" ", "%20")

        query_params = {
            'query': query,
            'format': file_type,
            'offset': offset,
            'count': count,
            'includeMetadata': include_metadata,
            'isMaskedResponse': is_masked_response
        }

        if self.py_client.version == SisenseVersion.Version.LINUX:
            self.py_client.connector.rest_call('get', 'api/datasources/{}/sql'
                                               .format(self.get_title(url_encoded=True)),
                                               query_params=query_params, path=path, raw=True)
        else:
            self.py_client.connector.rest_call('get', 'api/elasticubes/{}/sql'
                                               .format(self.get_title(url_encoded=True)),
                                               query_params=query_params, path=path, raw=True)
        return path

    def add_data_security_rule(self, table, column, data_type, *, shares=None, members=None,
                               server_address=None, exclusionary=False, all_members=None):
        """Define a data security rule

        Args:
            table (str): The table to apply security on
            column (str): The column to apply security on
            data_type (str): The data type of the column
            shares (list[Group,User]): (Optional) The users or groups to assign the security rule to.
                If none, will be 'everyone else' rule.
            members (list[str]): (Optional) An array of values which users should have access to
                If left blank, user will get 'Nothing'.
            server_address (str): (Optional) The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
                Use 'Set' for Elasticube Set. Required for elasticube sets.
            exclusionary (bool): (Optional) Set to True if exclusionary rule
            all_members (bool): (Optional) Set to True to set 'Everything' rule

        Returns:
             Rule: The new security rule
        """

        server_address = server_address if server_address else self.server_address

        rule_json = [{
            "column": column,
            "datatype": data_type,
            "table": table,
            "elasticube": self.get_title(),
            "server": server_address,
            "exclusionary": exclusionary,
            "allMembers": all_members
        }]

        shares_json = []
        if shares is None:
            # Default rule
            rule_json[0]['shares'] = [{"type": "default"}]
        else:
            for party in PySenseUtils.make_iterable(shares):
                if isinstance(party, PySenseUser.User):
                    shares_json.append({'party': party.get_id(), 'type': 'user'})
                elif isinstance(party, PySenseGroup.Group):
                    shares_json.append({'party': party.get_id(), 'type': 'group'})
                else:
                    raise PySenseException.PySenseException('{} is not a user or a group object'.format(party))
            rule_json[0]['shares'] = shares_json

        member_arr = []
        if members is None:
            rule_json[0]['members'] = []
            rule_json[0]['allMembers'] = False if all_members is None else all_members
        else:
            rule_json[0]['allMembers'] = None
            for member in members:
                member_arr.append(str(member))
            rule_json[0]['members'] = member_arr
        resp_json = self.py_client.connector.rest_call('post', 'api/elasticubes/{}/{}/datasecurity'
                                                       .format(server_address, self.get_title(url_encoded=True)),
                                                       json_payload=rule_json)

        return PySenseRule.Rule(self.py_client, resp_json[0])

    def get_data_security(self, *, server_address=None):
        """Return data security rules for the ElastiCube.

        Args:
            server_address (str): (Optional) The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
                Use 'Set' for Elasticube Set. Required for elasticube sets.

        Returns:
            list[Rule]: The data security rules for the ElastiCube
        """

        server_address = server_address if server_address else self.server_address

        resp_json = self.py_client.connector.rest_call('get', 'api/elasticubes/{}/{}/datasecurity'
                                                       .format(server_address, self.get_title(url_encoded=True)))
        ret_arr = []
        for rule in resp_json:
            ret_arr.append(PySenseRule.Rule(self.py_client, rule))
        return ret_arr

    def get_data_security_by_table_column(self, table, column, *, server_address=None):
        """Returns ElastiCube data security rules for a column in a table in the ElastiCube.

        Args:
            table (str): The name of the table in the ElastiCube
            column (str): The name of the column in the ElastiCube
            server_address (str): (Optional) The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
                Use 'Set' for Elasticube Set. Required for elasticube sets.

        Returns:
            list[Rule]: The data security rules for the table.column
        """

        server_address = server_address if server_address else self.server_address

        table = urllib.parse.quote(table)
        column = urllib.parse.quote(column)
        resp_json = self.py_client.connector.rest_call('get', 'api/elasticubes/{}/{}/datasecurity/{}/{}'
                                                       .format(server_address, self.get_title(url_encoded=True),
                                                                table, column))
        ret_arr = []
        for rule in resp_json:
            ret_arr.append(PySenseRule.Rule(self.py_client, rule))
        return ret_arr

    def get_data_security_for_user(self, user, *, server_address=None):
        """Returns an array of rules for the user on this cube

        Warning: There may be a Sisense side issue with this endpoint.

        Args:
            user (User): The user to fetch data security for
            server_address (str): (Optional) The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.

        Returns:
            list[Rule]: The data security rules for this user
        """

        server_address = server_address if server_address else self.server_address
        user_id = user.get_id()

        resp_json = self.py_client.connector.rest_call('get', 'api/elasticubes/{}/{}/{}/datasecurity'
                                                       .format(server_address, self.get_title(url_encoded=True),
                                                               user_id))
        ret_arr = []
        for rule in resp_json:
            ret_arr.append(PySenseRule.Rule(self.py_client, rule))
        return ret_arr

    def delete_data_security_rule(self, table, column, *, server_address=None):
        """Delete data security rule for a column.

        Args:
            table (str): The name of the table in the ElastiCube
            column (str): The name of the column in the ElastiCube
            server_address (str): (Optional) The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
                Use 'Set' for Elasticube Set. Required for elasticube sets.
        """

        server_address = server_address if server_address else self.server_address

        query_params = {
            'table': table,
            'column': column
        }
        self.py_client.connector.rest_call('delete', 'api/elasticubes/{}/{}/datasecurity'
                                           .format(server_address, self.get_title(url_encoded=True)),
                                           query_params=query_params)

    def get_oid(self):
        """Returns the Elasticube oid"""

        if 'oid' in self.json:
            return self.json['oid']
        elif '_id' in self.json:
            return self.json['_id']
        else:
            raise PySenseException('Cube {} is not currently running so this action cannot be performed')

    def get_metadata(self):
        """Get ElastiCube metadata"""

        query_params = {"q": self.get_title()}
        resp_json = self.py_client.connector.rest_call('get', 'api/elasticubes/metadata', query_params=query_params)
        if resp_json is None or len(resp_json) == 0:
            # If we don't get a response, it means the cube was never built so we return defaults
            return {
                "title": "",
                "fullname": "",
                "id": "",
                "address": "",
                "database": ""
            }
        return resp_json[0]

    def start_build(self, build_type, *, server_address=None, orchestrator_task=None):
        """Start cube build

        Windows only. For Linux use data models.

        Args:
            build_type (str): The build type (SchemaChanges, Accumulate, or Entire)
            server_address (str): (Optional) The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
            orchestrator_task (str): (Optional) The orchestrator task

        """

        PySenseUtils.validate_version(self.py_client, SisenseVersion.Version.WINDOWS, 'start_build')

        query_params = {
            'type': build_type,
            'orchestratorTask': orchestrator_task

        }
        server_address = server_address if server_address else self.server_address
        self.py_client.connector.rest_call('post', 'api/elasticubes/{}/{}/startBuild'
                                           .format(server_address, self.get_title(url_encoded=True)),
                                           query_params=query_params)

    def stop_build(self, *, server_address=None):
        """Stop cube build

        Windows only

        Args:
            server_address: (Optional) The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
        """

        PySenseUtils.validate_version(self.py_client, SisenseVersion.Version.WINDOWS, 'stop_build')

        server_address = server_address if server_address else self.server_address
        self.py_client.connector.rest_call('post', 'api/elasticubes/{}/{}/stopBuild'
                                           .format(server_address, self.get_title(url_encoded=True)))

    def stop_cube(self, *, server_address=None):
        """Stop cube

        Windows only

        Args:
            server_address (str): (Optional) The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
        """

        PySenseUtils.validate_version(self.py_client, SisenseVersion.Version.WINDOWS, 'stop_cube')

        server_address = server_address if server_address else self.server_address
        self.py_client.connector.rest_call('post', 'api/elasticubes/{}/{}/stop'
                                           .format(server_address, self.get_title(url_encoded=True)))

    def start_cube(self, *, server_address=None):
        """Start cube

        Windows only

        Args:
            server_address (str): (Optional) The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
        """

        PySenseUtils.validate_version(self.py_client, SisenseVersion.Version.WINDOWS, 'start_cube')

        server_address = server_address if server_address else self.server_address
        self.py_client.connector.rest_call('post', 'api/elasticubes/{}/{}/start'
                                           .format(server_address, self.get_title(url_encoded=True)))

    def restart_cube(self, *, server_address=None):
        """Start cube

        Windows only

        Args:
            server_address (str): (Optional) The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
        """

        PySenseUtils.validate_version(self.py_client, SisenseVersion.Version.WINDOWS, 'restart_cube')

        server_address = server_address if server_address else self.server_address
        self.py_client.connector.rest_call('post', 'api/elasticubes/{}/{}/restart'
                                           .format(server_address, self.get_title(url_encoded=True)))

    def add_share(self, shares, *, can_edit=False):
        """Share a cube to new groups and users

        By default will give query access. Set can_edit to True for editor access.

        Args:
            shares (list[Group,User]): Users and groups to share the cube to
            can_edit (bool): (Optional) True for edit privileges
        """

        shares = PySenseUtils.make_iterable(shares)
        curr_shares_arr = self.get_shares_json()
        rule = 'r' if can_edit is False else 'w'
        curr_id_arr = []
        for share in curr_shares_arr:
            party_id = share['partyId']
            curr_id_arr.append(party_id)
            del share['partyId']
            share['party'] = party_id

        for share in shares:
            share_id = share.get_id()
            if share_id is None:
                raise PySenseException.PySenseException('No id found for {}'.format(share))
            elif share_id in curr_id_arr:
                index = curr_id_arr.index(share_id)
                curr_shares_arr[index]['permission'] = rule
            elif isinstance(share, PySenseUser.User):
                curr_shares_arr.append({'party': share.get_id(), 'type': 'user', 'permission': rule})
            elif isinstance(share, PySenseGroup.Group):
                curr_shares_arr.append({'party': share.get_id(), 'type': 'group', 'rule': rule})
            else:
                raise PySenseException.PySenseException('Add Share expected User or group, got {}'.format(type(share)))

        self.py_client.connector.rest_call('put', 'api/elasticubes/{}/{}/permissions'
                                           .format(self.server_address, self.get_title(url_encoded=True)),
                                           json_payload=curr_shares_arr)

    def remove_shares(self, shares):
        """Unshare a cube to groups and users

        To unshare a cube we have to:
            - Query for the whom the cube is currently shared with
            - Delete the users/groups we want to unshare with
            - Re upload the reduced share

        Args:
            shares (list[Group,User]): Users and groups to unshare the cube to
        """

        curr_shares_arr = self.get_shares_json()
        curr_id_arr = []
        for share in curr_shares_arr:
            curr_id_arr.append(share['partyId'])

        for share in PySenseUtils.make_iterable(shares):
            share_id = share.get_id()
            if share_id is None:
                raise PySenseException.PySenseException('No id found for {}'.format(share))
            elif share_id in curr_id_arr:
                index = curr_id_arr.index(share_id)
                del curr_shares_arr[index]
                del curr_id_arr[index]

        self.py_client.connector.rest_call('put', 'api/elasticubes/{}/{}/permissions'
                                           .format(self.server_address, self.get_title(url_encoded=True)),
                                           json_payload=curr_shares_arr)

    def get_shares_json(self):
        """Returns the shares of the elasticube as JSON"""
        resp = self.py_client.connector.rest_call('get', 'api/elasticubes/{}/{}/permissions'
                                                  .format(self.server_address, self.get_title(url_encoded=True)))
        return resp["shares"]

    def get_shares_user_group(self):
        """Returns the shares of the elasticube as users and groups

        Returns:
            list[User,Group]: Users and groups this elasticube is shared with
        """

        ret_arr = []
        for share in self.get_shares_json():
            if share['type'] == 'user':
                ret_arr.append(self.py_client.get_user_by_id(share['partyId']))
            elif share['type'] == 'group':
                ret_arr.append(self.py_client.get_group_by_id(share['partyId']))
        return ret_arr
