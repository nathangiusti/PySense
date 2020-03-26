import requests
import urllib.parse

from PySense import PySenseGroup
from PySense import PySenseRule
from PySense import PySenseUser
from PySense import PySenseUtils


class Elasticube:

    def __init__(self, host, token, cube_json):
        self._host = host
        self._token = token
        self._cube_json = cube_json
        self._host_formatted = self._host.split('//')[1].split(':')[0]

    def get_name(self):
        return self._cube_json['title']

    def get_data_source_sql(self, query, file_type, *, path=None,
                            offset=None, count=None, include_metadata=None, is_masked_response=None):
        """
        Executes elasticube sql. This is a non public API. This functionality is beta
        Seems to only work on localhost

        :param path: The location to save the file
        :param query: The query to execute
        :param file_type: File format to return
        :param offset: Defines how many items to skip before returning the results.
            For example, to return results from value #101 onward, enter a value of ‘100’.
        :param count: Limits the result set to a defined number of results. Enter 0 (zero) or leave blank not to limit.
        :param include_metadata: Whether to include metadata.
        :param is_masked_response: Whether response should be masked.
        :return: The path of the created file or the content payload if path is None
        """

        query = urllib.parse.quote(query)

        param_string = PySenseUtils.build_query_string({
            'query': query,
            'format': file_type,
            'offset': offset,
            'count': count,
            'includeMetadata': include_metadata,
            'isMaskedResponse': is_masked_response
        })
        print('{}/api/datasources/{}/{}/sql?{}'.format(
            self._host, self._host_formatted, urllib.parse.quote(self.get_name()), param_string))
        resp = requests.get('{}/api/datasources/{}/{}/sql?{}'.format(
            self._host, self._host_formatted, urllib.parse.quote(self.get_name()), param_string), headers=self._token)
        PySenseUtils.parse_response(resp)
        output = resp.content.decode('utf-8-sig').splitlines()
        if path is not None:
            with open(path, "w") as file:
                for line in output:
                    file.write(line + '\n')
            return path
        else:
            return output

    def add_security_rule(self, shares, table, column, data_type, members, *, exclusionary=False, all_members=None):
        """
        Defines data security rules for a column on a specific server and elasticube

        :param shares: The users or groups to assign the security rule to
        :param table: The table to apply security on
        :param column: The column to apply security on
        :param data_type: The data type of the column
        :param members: An array of values which users should have access to
        :param exclusionary: True if exclusionary rule
        :param all_members: True if all members to be selectable
        :return:
        """

        rule_json = [{
                        "column": column,
                        "datatype": data_type,
                        "table": table,
                        "elasticube": self.get_name(),
                        "server": self._host_formatted,
                        "exclusionary": exclusionary,
                        "allMembers": all_members
                    }]

        shares_json = []
        for party in shares:
            if isinstance(party, PySenseUser.User):
                shares_json.append({'party': party.get_user_id(), 'type': 'user'})
            elif isinstance(party, PySenseGroup.Group):
                shares_json.append({'party': party.get_group_id(), 'type': 'group'})
        rule_json[0]['shares'] = shares_json

        member_arr = []
        for member in members:
            member_arr.append(str(member))
        rule_json[0]['members'] = member_arr

        resp = requests.post('{}/api/elasticubes/{}/{}/datasecurity'.format(
            self._host, self._host_formatted, urllib.parse.quote(self.get_name())), headers=self._token, json=rule_json)
        PySenseUtils.parse_response(resp)

        return PySenseRule.Rule(self._host, self._token, resp.json()[0])

    def get_elasticube_datasecurity(self):
        """
        Return data security rules for the elasticube
        :return: The data security rules for the elasticube
        """
        resp = requests.get('{}/api/elasticubes/{}/{}/datasecurity'.format(
            self._host, self._host_formatted, urllib.parse.quote(self.get_name())), headers=self._token)
        PySenseUtils.parse_response(resp)
        ret_arr = []
        for rule in resp.json():
            ret_arr.append(PySenseRule.Rule(self._host, self._token, rule))
        return ret_arr

    def get_elasticube_datasecurity_by_table_column(self, table, column):
        """
        Returns ElastiCube data security rules for a column in a table in the ElastiCube

        :param table: The name of the table in the ElastiCube
        :param column: The name of the column in the ElastiCube
        :return:
        """
        resp = requests.get('{}/api/elasticubes/{}/{}/datasecurity/{}/{}'.format(
            self._host, self._host_formatted, urllib.parse.quote(self.get_name()), table, column), headers=self._token)
        PySenseUtils.parse_response(resp)
        ret_arr = []
        for rule in resp.json():
            ret_arr.append(PySenseRule.Rule(self._host, self._token, rule))
        return ret_arr

    def delete_rule(self, table, column):
        """
        Delete data security rule for a column
        :param table: The name of the table in the ElastiCube
        :param column: The name of the column in the ElastiCube
        :return: True
        """
        param_string = PySenseUtils.build_query_string({
            'table': table,
            'column': column
        })
        resp = requests.delete('{}/api/elasticubes/{}/{}/datasecurity?{}'.format(
            self._host, self._host_formatted, urllib.parse.quote(self.get_name()), param_string), headers=self._token)
        PySenseUtils.parse_response(resp)
        return True
