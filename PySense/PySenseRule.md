Module PySense.PySenseRule
==========================

Classes
-------

`Rule(host, token, rule_json)`
:   

    ### Methods

    `get_member_values(self)`
    :   Gets the member values
        :return: The member values

    `get_rule_id(self)`
    :   Gets the rule id
        :return: The rule id

    `update_rule(self, shares, table, column, data_type, members, *, exclusionary=False, all_members=None)`
    :   Updates the current rule
        :param shares: Array of users and groups to share the rule with
        :param table: Table of the data security rule
        :param column: Column of the data security rule
        :param data_type: Data security rule data type
        :param members: The values to specify in the rule
        :param exclusionary: Set to true to make an exclusionary rule
        :param all_members: Set to true for a rule to allow user to see all values
        :return: True