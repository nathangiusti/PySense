from PySense import PySenseGroup
from PySense import PySenseUser
from PySense import PySenseUtils


class Rule:
    def __init__(self, connector, rule_json):
        self._connector = connector
        self._reset(rule_json)

    def _reset(self, rule_json):
        # Sisense returns partyId in the object response, but wants party for the request. So we fix that here.
        for share in rule_json['shares']:
            if 'partyId' in share:
                share['party'] = share.pop('partyId')
        self._rule_json = rule_json

    def get_shares(self):
        return self._rule_json['shares']
    
    def get_id(self):
        """  
        Gets the rule id  

        :return: The rule id  
        """

        return self._rule_json['_id']
    
    def get_column(self):
        """  
        Gets the column for which the rule applies  
          
        :return: The column title  
        """  
        
        return self._rule_json['column']

    def get_table(self):
        """  
        Gets the table for which the rule applies  

        :return: The table title  
        """

        return self._rule_json['table']

    def get_members(self):
        """
        Gets the member values  
          
        :return: The member values  
        """
        
        return self._rule_json['members']
    
    def get_data_type(self):
        """  
        Gets the data type for which the rule applies  

        :return: The rule data type
        """

        return self._rule_json['datatype']
    
    def get_exclusionary(self):
        """  
        Returns whether or not the rule is exclusionary  

        :return: True if exclusionary, None or false otherwise  
        """

        return self._rule_json['exclusionary']
    
    def get_all_members(self):
        """  
        Returns whether or not the rule is for all members

        :return: True if for all_members, None or false otherwise
        """

        return self._rule_json['exclusionary']
        
    def update_rule(self, *, shares=None, table=None, column=None, data_type=None, members=None, 
                    exclusionary=None, all_members=None):
        """
        Updates the current rule. Any arguments given will replace the current value and update the rule  
        
        Optional: 
        :param shares: Array of users and groups to share the rule with  
        :param table: Table of the data security rule  
        :param column: Column of the data security rule  
        :param data_type: Data security rule data type  
        :param members: The values to specify in the rule. If blank, will use nothing
        :param exclusionary: Set to true to make an exclusionary rule  
        :param all_members: Set to true for a rule to allow user to see all values  
        """
        rule_json = {
            "column": column if column is not None else self.get_column(),
            "datatype": data_type if data_type is not None else self.get_data_type(),
            "table": table if table is not None else self.get_table(),
            "exclusionary": exclusionary if table is not None else self.get_exclusionary(),
            "allMembers": all_members if all_members is not None else self.get_all_members(),
        }
        shares_json = []
        if shares is not None:
            for party in PySenseUtils.make_iterable(shares):
                if isinstance(party, PySenseUser.User):
                    shares_json.append({'party': party.get_id(), 'type': 'user'})
                elif isinstance(party, PySenseGroup.Group):
                    shares_json.append({'party': party.get_id(), 'type': 'group'})
            rule_json['shares'] = shares_json
        else:
            rule_json['shares'] = self.get_shares()

        if members is not None:
            member_arr = []
            for member in PySenseUtils.make_iterable(members):
                member_arr.append(str(member))
            rule_json['members'] = member_arr
        else:
            rule_json['members'] = self.get_members()
        
        resp_json = self._connector.rest_call('put', 'api/elasticubes/datasecurity/{}'.format(self.get_id()),
                                              json_payload=rule_json)
        self._reset(resp_json)
