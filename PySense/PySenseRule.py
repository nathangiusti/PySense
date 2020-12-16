from PySense import PySenseGroup, PySenseUser, PySenseUtils


class Rule:
    """A data security rule

    A rule belongs to a single table.column
    A column may have multiple rules. A rule belongs to a single table.column
    Each rule has a list of groups and users that the rule applies to

    Attributes:
        json (JSON): The JSON for this object
        py_client (PySense): The connection to the Sisense server which owns this asset
    """

    def __init__(self, py_client, rule_json):
        """

        Args:
            py_client (PySense): The PySense object for the server this asset belongs to
            rule_json (JSON): The json for this object
        """

        self.py_client = py_client
        self._reset(rule_json)

    def _reset(self, rule_json):
        # Sisense returns partyId in the object response, but wants party for the request. So we fix that here.
        for share in rule_json['shares']:
            if 'partyId' in share:
                share['party'] = share.pop('partyId')
        self._rule_json = rule_json

    def get_shares_json(self):
        """Returns the rules shares as JSON"""

        return self._rule_json['shares']

    def get_shares_user_groups(self):
        """Returns the rules shares as users and groups

        Returns:
            list[User,Group]: Users and groups this rule is applied to
        """
        ret_arr = []
        for share in self._rule_json['shares']:
            if share['type'] == 'user':
                ret_arr.append(self.py_client.get_user_by_id(share['party']))
            elif share['type'] == 'group':
                ret_arr.append(self.py_client.get_group_by_id(share['party']))
        return ret_arr

    def get_id(self):
        """Gets the rule id."""

        return self._rule_json['_id']

    def get_column(self):
        """Gets the column for which the rule applies"""

        return self._rule_json['column']

    def get_table(self):
        """Gets the table for which the rule applies."""

        return self._rule_json['table']

    def get_members(self):
        """Gets the member values."""

        return self._rule_json['members']

    def get_data_type(self):
        """Gets the data type for which the rule applies."""

        return self._rule_json['datatype']

    def get_exclusionary(self):
        """Returns whether or not the rule is exclusionary"""

        return self._rule_json['exclusionary']

    def get_all_members(self):
        """Returns whether or not the rule is for all members."""

        return self._rule_json['exclusionary']

    def update_rule(self, *, table=None, column=None, data_type=None, shares='', members='',
                    exclusionary='', all_members=''):
        """Updates the current rule.

        Any arguments given will replace the current value and update the rule in place

        Args:
            shares (list[User,Group]): (Optional) Array of users and groups to share the rule with
            table (str): (Optional) Table of the data security rule
            column (str): (Optional) Column of the data security rule
            data_type (str): (Optional) Data security rule data type
            members (list[str]): (Optional) The values to specify in the rule. If blank, will use nothing
            exclusionary (bool): (Optional) Set to true to make an exclusionary rule
            all_members (bool): (Optional) Set to true for a rule to allow user to see all values
        """

        rule_json = {
            "column": column if column is not None else self.get_column(),
            "datatype": data_type if data_type is not None else self.get_data_type(),
            "table": table if table is not None else self.get_table(),
            "exclusionary": exclusionary if exclusionary != '' else self.get_exclusionary(),
            "allMembers": all_members if all_members != '' else self.get_all_members(),
        }
        shares_json = []
        if shares != '':
            for party in PySenseUtils.make_iterable(shares):
                if isinstance(party, PySenseUser.User):
                    shares_json.append({'party': party.get_id(), 'type': 'user'})
                elif isinstance(party, PySenseGroup.Group):
                    shares_json.append({'party': party.get_id(), 'type': 'group'})
            rule_json['shares'] = shares_json
        else:
            rule_json['shares'] = self.get_shares_json()

        if members != '':
            if members is None:
                rule_json['members'] = []
                rule_json['allMembers'] = False if all_members == '' else all_members
            else:
                member_arr = []
                for member in PySenseUtils.make_iterable(members):
                    member_arr.append(str(member))
                rule_json['members'] = member_arr
                rule_json['allMembers'] = None
        else:
            rule_json['members'] = self.get_members()

        resp_json = self.py_client.connector.rest_call('put', 'api/elasticubes/datasecurity/{}'.format(self.get_id()),
                                                       json_payload=rule_json)
        self._reset(resp_json)
