from PySense import PySenseGroup, PySenseUser, PySenseUtils


class Rule:
    def __init__(self, py_client, rule_json):
        self._py_client = py_client
        self._reset(rule_json)

    def _reset(self, rule_json):
        # Sisense returns partyId in the object response, but wants party for the request. So we fix that here.
        for share in rule_json['shares']:
            if 'partyId' in share:
                share['party'] = share.pop('partyId')
        self._rule_json = rule_json

    def get_shares(self):
        """Returns the rules shares"""
        return self._rule_json['shares']

    def get_id(self):
        """Gets the rule id."""
        return self._rule_json['_id']

    def get_column(self):
        """Gets the column for which the rule applies"""
        return self._rule_json['column']

    def get_table(self):
        """ Gets the table for which the rule applies."""
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
            shares: (optional) Array of users and groups to share the rule with
            table: (optional) Table of the data security rule
            column: (optional) Column of the data security rule
            data_type: (optional) Data security rule data type
            members: (optional) The values to specify in the rule. If blank, will use nothing
            exclusionary: (optional) Set to true to make an exclusionary rule
            all_members: (optional) Set to true for a rule to allow user to see all values
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
            rule_json['shares'] = self.get_shares()

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

        resp_json = self._py_client.connector.rest_call('put', 'api/elasticubes/datasecurity/{}'.format(self.get_id()),
                                                        json_payload=rule_json)
        self._reset(resp_json)
