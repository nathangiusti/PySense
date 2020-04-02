Module PySense.PySenseUser
==========================

Classes
-------

`User(host, token, user_json)`
:   

    ### Methods

    `get_user_id(self)`
    :   Returns the user's id
        :return: The user id

    `get_user_user_name(self)`
    :   Returns the user's username
        :return: The user's username

    `update_user(self, *, email=None, user_name=None, first_name=None, last_name=None, role_name=None, groups=None, preferences=None, ui_settings=None)`
    :   Updates given fields for user object. Returns true if successful, None if error
        
        @param email: Value to update email to
        @param user_name: Value to update username to
        @param first_name: Value to update firstName to
        @param last_name: Value to update lastName to
        @param role_name: New role for user
        @param groups: Groups to put user in
        @param preferences: Preferences to be updated for user
        @param ui_settings: UI Settings to be updated for user
        @return: True if successful