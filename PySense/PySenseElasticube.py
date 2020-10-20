import random
import urllib.parse

from PySense import SisenseVersion
from PySense import PySenseDataModel
from PySense import PySenseException
from PySense import PySenseGroup
from PySense import PySenseRule
from PySense import PySenseUser
from PySense import PySenseUtils
from PySense import PySenseFormula


class Elasticube:

    def __init__(self, py_client, cube_json):
        self._cube_json = cube_json
        self._py_client = py_client
        self._server_address = 'localhost'
        if py_client.version == SisenseVersion.Version.WINDOWS:
            metadata = self.get_metadata()
            if metadata is None:
                print('No meta data for cube {}'.format(self.get_title()))
            elif 'address' in metadata:
                self._server_address = metadata['address']
            elif metadata['fullname'].endswith(' - Set'):
                self._server_address = 'Set'

    def get_oid(self):
        """Returns the Elasticube id"""
        if 'oid' in self._cube_json:
            return self._cube_json['oid']
        else:
            raise PySenseException('Cube {} is not currently running so this action cannot be performed')

    def get_model(self, path=None):
        """Returns the data model object for the cube.

        Args:
            - (Optional) path: The file location to save the smodel file to

        Returns:
            A data model or the file path if the file path is set.
        """

        query_params = {'datamodelId': self.get_oid(), 'type': 'schema-latest'}
        if path is not None:
            resp_content = self._py_client.connector.rest_call('get', 'api/v2/datamodel-exports/schema',
                                                               query_params=query_params, raw=True)
            with open(path, 'wb') as out_file:
                out_file.write(resp_content)
            return path
        else:
            data_model_json = self._py_client.connector.rest_call(
                'get', 'api/v2/datamodel-exports/schema', query_params=query_params)
            data_model_json['oid'] = self.get_oid()
            return PySenseDataModel.DataModel(self._py_client, data_model_json)

    def get_title(self, url_encoded=False):
        """Returns the ElastiCube's title.

        Args:
            - (Optional) url_encoded: True to url encode the name. Use for passing as query parameter.

        Returns:
             The name of the ElastiCube, url encoded if set.
        """
        if url_encoded:
            return urllib.parse.quote(self._cube_json['title'])
        else:
            return self._cube_json['title']

    def run_sql(self, query, file_type, *, path=None,
                offset=None, count=None, include_metadata=None, is_masked_response=None):
        """Executes SQL against ElastiCube.

        Args:
            - query: The query to execute
            - file_type: File format to return
            - (Optional) path: The location to save the file
            - (Optional) offset: Defines how many items to skip before returning the results.
                For example, to return results from value #101 onward, enter a value of ‘100’.
            - (Optional) count: Limits the result set to a defined number of results. Enter 0 (zero) or leave blank not to limit.
            - (Optional) include_metadata: Whether to include metadata.
            - (Optional) is_masked_response: Whether response should be masked.

        Returns:
             The path of the created file or the content payload if path is None
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

        if self._py_client.version == SisenseVersion.Version.LINUX:
            resp_content = self._py_client.connector.rest_call('get', 'api/datasources/{}/sql'
                                                               .format(self.get_title(url_encoded=True)),
                                                               query_params=query_params, raw=True)
        else:
            resp_content = self._py_client.connector.rest_call('get', 'api/elasticubes/{}/sql'
                                                               .format(self.get_title(url_encoded=True)),
                                                               query_params=query_params, raw=True)
        output = resp_content.decode('utf-8-sig').splitlines()
        if path is not None:
            with open(path, "w") as file:
                for line in output:
                    file.write(line + '\n')
            return path
        else:
            return resp_content

    def add_security_rule(self, table, column, data_type, *, shares=None, members=None,
                          server_address=None, exclusionary=False, all_members=None):
        """Defines data security rules for a column on a specific server and ElastiCube

        Args:
            - table: The table to apply security on
            - column: The column to apply security on
            - data_type: The data type of the column
            - (Optional) shares: The users or groups to assign the security rule to. If none, will be default rule.
            - (Optional) members: An array of values which users should have access to
                If left blank, user will get none.
            - (Optional) server_address: The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
                Use 'Set' for Elasticube Set. Required for elasticube sets.
            - (Optional) exclusionary: True if exclusionary rule
            - (Optional) all_members: True if all members to be selectable

        Returns:
             The new security rule
        """
        server_address = server_address if server_address else self._server_address

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
        resp_json = self._py_client.connector.rest_call('post', 'api/elasticubes/{}/{}/datasecurity'
                                                        .format(server_address, self.get_title(url_encoded=True)),
                                                        json_payload=rule_json)

        return PySenseRule.Rule(self._py_client, resp_json[0])

    def get_datasecurity(self, *, server_address=None):
        """Return data security rules for the ElastiCube.

        Args:
            - (Optional) server_address: The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
                Use 'Set' for Elasticube Set. Required for elasticube sets.

        Returns:
            The data security rules for the ElastiCube
        """
        server_address = server_address if server_address else self._server_address

        resp_json = self._py_client.connector.rest_call('get', 'api/elasticubes/{}/{}/datasecurity'
                                                        .format(server_address, self.get_title(url_encoded=True)))
        ret_arr = []
        for rule in resp_json:
            ret_arr.append(PySenseRule.Rule(self._py_client, rule))
        return ret_arr

    def get_datasecurity_by_table_column(self, table, column, *, server_address=None):
        """Returns ElastiCube data security rules for a column in a table in the ElastiCube.

        Args:
            - table: The name of the table in the ElastiCube
            - column: The name of the column in the ElastiCube
            - (Optional) server_address: The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
                Use 'Set' for Elasticube Set. Required for elasticube sets.

        Returns:
            An array of security rules.
        """

        server_address = server_address if server_address else self._server_address

        table = urllib.parse.quote(table)
        column = urllib.parse.quote(column)
        resp_json = self._py_client.connector.rest_call('get', 'api/elasticubes/{}/{}/datasecurity/{}/{}'
                                                        .format(server_address, self.get_title(url_encoded=True),
                                                                table, column))
        ret_arr = []
        for rule in resp_json:
            ret_arr.append(PySenseRule.Rule(self._py_client, rule))
        return ret_arr

    def get_datasecurity_for_user(self, user, *, server_address=None):
        """Returns an array of rules for the user on this cube

        Args:
            - user: The user id, username, or user obect
            - (Optional) server_address: The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.

        Returns:
            An array of PySense Rules
        """

        server_address = server_address if server_address else self._server_address

        if isinstance(user, PySenseUser.User):
            user_id = user.get_id()
        else:
            user_id = urllib.parse.quote(user)
        resp_json = self._py_client.connector.rest_call('get', 'api/elasticubes/{}/{}/{}/datasecurity'
                                                        .format(server_address, self.get_title(url_encoded=True),
                                                                user_id))
        ret_arr = []
        for rule in resp_json:
            ret_arr.append(PySenseRule.Rule(self._py_client, rule))
        return ret_arr

    def delete_rule(self, table, column, *, server_address=None):
        """Delete data security rule for a column.

        Args:
            - table: The name of the table in the ElastiCube
            - column: The name of the column in the ElastiCube
            - server_address (Optional): The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
                Use 'Set' for Elasticube Set. Required for elasticube sets.
        """
        server_address = server_address if server_address else self._server_address

        query_params = {
            'table': table,
            'column': column
        }
        self._py_client.connector.rest_call('delete', 'api/elasticubes/{}/{}/datasecurity'
                                            .format(server_address, self.get_title(url_encoded=True)),
                                            query_params=query_params)

    def get_oid(self):
        """Returns the Elasticube id"""
        if 'oid' in self._cube_json:
            return self._cube_json['oid']
        elif '_id' in self._cube_json:
            return self._cube_json['_id']
        else:
            raise PySenseException('Cube {} is not currently running so this action cannot be performed')

    def get_saved_formulas(self, *, server_address=None):
        """Get elasticube formulas.

        Args:
            - (Optional) server_address: The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.

        Returns:
             An array of formulas
        """
        server_address = server_address if server_address else self._server_address
        query_params = {
            'datasource': self.get_title(url_encoded=True),
            'server': server_address
        }
        resp_json = self._py_client.connector.rest_call('get', 'api/metadata/measures', query_params=query_params)
        ret_arr = []
        for formula in resp_json:
            ret_arr.append(PySenseFormula.Formula(self._py_client, formula))

        return ret_arr

    def delete_formulas(self, formulas):
        """Delete given formulas from ElastiCube"""

        for formula in PySenseUtils.make_iterable(formulas):
            self._py_client.connector.rest_call('delete', 'api/metadata/{}'.format(formula.get_oid()))

    def get_metadata(self):
        """Get ElastiCube metadata"""
        query_params = {"q": self.get_title()}
        resp_json = self._py_client.connector.rest_call('get', 'api/elasticubes/metadata', query_params=query_params)
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

    def add_formula_to_cube(self, formulas):
        """Add formulas to cube"""
        for formula in PySenseUtils.make_iterable(formulas):
            formula.change_datasource(self)
            elements_to_remove = ['_id', 'created', 'lastUpdated', 'oid']
            formula_json = formula.get_json()
            for element in elements_to_remove:
                formula_json.pop(element, None)
            self._py_client.connector.rest_call('post', 'api/metadata', json_payload=formula_json)

    def start_build(self, build_type, *, server_address=None, orchestrator_task=None):
        """Start cube build

        Windows only

        - Args
            - build_type: The build type (SchemaChanges, Accumulate, or Entire)
            - (Optional) server_address: The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
            - (Optional) orchestrator_task:

        """
        PySenseUtils.validate_version(self._py_client, SisenseVersion.Version.WINDOWS, 'start_build')

        query_params = {
            'type': build_type,
            'orchestratorTask': orchestrator_task

        }
        server_address = server_address if server_address else self._server_address
        self._py_client.connector.rest_call('post', 'api/elasticubes/{}/{}/startBuild'
                                            .format(server_address, self.get_title(url_encoded=True)),
                                            query_params=query_params)

    def stop_build(self, *, server_address=None):
        """Stop cube build

        Windows only

        - Args
            - (Optional) server_address: The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
        """
        PySenseUtils.validate_version(self._py_client, SisenseVersion.Version.WINDOWS, 'stop_build')

        server_address = server_address if server_address else self._server_address
        self._py_client.connector.rest_call('post', 'api/elasticubes/{}/{}/stopBuild'
                                            .format(server_address, self.get_title(url_encoded=True)))

    def stop_cube(self, *, server_address=None):
        """Stop cube

        Windows only

        - Args
            - (Optional) server_address: The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
        """
        PySenseUtils.validate_version(self._py_client, SisenseVersion.Version.WINDOWS, 'stop_cube')

        server_address = server_address if server_address else self._server_address
        self._py_client.connector.rest_call('post', 'api/elasticubes/{}/{}/stop'
                                            .format(server_address, self.get_title(url_encoded=True)))

    def start_cube(self, *, server_address=None):
        """Start cube

        Windows only

        - Args
            - (Optional) server_address: The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
        """
        PySenseUtils.validate_version(self._py_client, SisenseVersion.Version.WINDOWS, 'start_cube')

        server_address = server_address if server_address else self._server_address
        self._py_client.connector.rest_call('post', 'api/elasticubes/{}/{}/start'
                                            .format(server_address, self.get_title(url_encoded=True)))

    def restart_cube(self, *, server_address=None):
        """Start cube

        Windows only

        - Args
            - (Optional) server_address: The server address of the ElastiCube.
                Set this to your server ip if this method fails without it set.
        """
        PySenseUtils.validate_version(self._py_client, SisenseVersion.Version.WINDOWS, 'restart_cube')

        server_address = server_address if server_address else self._server_address
        self._py_client.connector.rest_call('post', 'api/elasticubes/{}/{}/restart'
                                            .format(server_address, self.get_title(url_encoded=True)))

    def add_share(self, shares, *, can_edit=False):
        """Share a cube to new groups and users

        By default will give query access. Set can_edit to True for editor access.

        Args:
            shares: One to many PySense Groups and Users
            can_edit: (Optional) True for edit privileges, False or default for query privileges.
        """

        shares = PySenseUtils.make_iterable(shares)
        curr_shares_arr = self.get_shares()['shares']
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

        self._py_client.connector.rest_call('put', 'api/elasticubes/{}/{}/permissions'
                                            .format(self._server_address, self.get_title(url_encoded=True)),
                                            json_payload=curr_shares_arr)

    def remove_shares(self, shares):
        """Unshare a cube to groups and users

        Args:
            shares: One to many PySense Groups and Users
        """
        shares = PySenseUtils.make_iterable(shares)
        curr_shares_arr = self.get_shares()['shares']
        curr_id_arr = []
        for share in curr_shares_arr:
            curr_id_arr.append(share['partyId'])

        for share in shares:
            share_id = share.get_id()
            if share_id is None:
                raise PySenseException.PySenseException('No id found for {}'.format(share))
            elif share_id in curr_id_arr:
                index = curr_id_arr.index(share_id)
                del curr_shares_arr[index]
                del curr_id_arr[index]

        self._py_client.connector.rest_call('put', 'api/elasticubes/{}/{}/permissions'
                                            .format(self._server_address, self.get_title(url_encoded=True)),
                                            json_payload=curr_shares_arr)

    def get_shares(self):
        """Returns the shares of the elasticube"""
        return self._py_client.connector.rest_call('get', 'api/elasticubes/{}/{}/permissions'
                                                   .format(self._server_address, self.get_title(url_encoded=True)))

    def get_address(self):
        """Returns the server address from the elasticube metadata"""
        return self._server_address
