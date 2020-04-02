Module PySense.PySenseGroup
===========================

Classes
-------

`Group(host, token, group_json)`
:   

    ### Methods

    `add_user_to_group(self, users)`
    :   Adds users to group
        :param users: List of users to add
        :return: True

    `delete_user_from_group(self, users)`
    :   Remove users from group
        :param users: Users to remove
        :return: True

    `get_group_id(self)`
    :   Get groups id
        :return: The id of the group

    `get_group_name(self)`
    :   Get groups name
        :return: The name of the group