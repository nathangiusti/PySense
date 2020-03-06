import requests

from PySense import PySenseGroup
from PySense import PySenseUser
from PySense import PySenseUtils


class Rule:
    def __init__(self, host, token, rule_json):
        self._host = host
        self._token = token
        self._reset(rule_json)

    def _reset(self, rule_json):
        for share in rule_json['shares']:
            if 'partyId' in share:
                share['party'] = share.pop('partyId')
        self._rule_json = rule_json

    def get_rule_id(self):
        """
        Gets the rule id
        :return: The rule id
        """
        return self._rule_json['_id']

    def get_member_values(self):
        """
        Gets the member values
        :return: The member values
        """
        return self._rule_json['members']

    def update_rule(self, shares, table, column, data_type, members, *, exclusionary=False, all_members=None):
        """
        Updates the current rule
        :param shares: Array of users and groups to share the rule with
        :param table: Table of the data security rule
        :param column: Column of the data security rule
        :param data_type: Data security rule data type
        :param members: The values to specify in the rule
        :param exclusionary: Set to true to make an exclusionary rule
        :param all_members: Set to true for a rule to allow user to see all values
        :return: True
        """
        rule_json = {
            "column": column,
            "datatype": data_type,
            "table": table,
            "exclusionary": exclusionary,
            "allMembers": all_members
        }

        shares_json = []
        for party in shares:
            if isinstance(party, PySenseUser.User):
                shares_json.append({'party': party.get_user_id(), 'type': 'user'})
            elif isinstance(party, PySenseGroup.Group):
                shares_json.append({'party': party.get_group_id(), 'type': 'group'})
        rule_json['shares'] = shares_json

        member_arr = []
        for member in members:
            member_arr.append(str(member))
        rule_json['members'] = member_arr

        resp = requests.put('{}/api/elasticubes/datasecurity/{}'.format(
            self._host, self.get_rule_id()), headers=self._token, json=rule_json)
        PySenseUtils.parse_response(resp)
        self._reset(resp.json())
        return True

