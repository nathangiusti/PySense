import json
import requests

import PySenseUtils


class User:

    def __init__(self, host, token, user_json):
        self.host = host
        self.token = token
        self.user_json = user_json
        self.user_id = user_json['_id']

    def reset(self, user_json):
        self.user_json = user_json
        self.user_id = user_json['_id']

    def get_user_id(self):
        return self.user_id

    def update_user(self, email=None, userName=None, firstName=None, lastName=None, role=None, groups=None,
                    preferences=None, uiSettings=None):
        """
        Updates given fields for user object. Returns true if successful, None if error

        @param email: Value to update email to
        @param userName: Value to update username to
        @param firstName: Value to update firstName to
        @param lastName: Value to update lastName to
        @param role: New role for user
        @param groups: Groups to put user in
        @param preferences: Preferences to be updated for user
        @param uiSettings: UI Settings to be updated for user
        @return:
        """
        role_id = PySenseUtils.get_role_id(self.host, self.token, role)
        if not role_id:
            return "Role {} not found".format(role)
        json_obj = PySenseUtils.build_json_object(
            {
                'email': email,
                'userName': userName,
                'firstName': firstName,
                'lastName': lastName,
                'role': role_id,
                'groups': groups,
                'preferences': preferences,
                'uiSettings': uiSettings
            }
        )
        resp = requests.patch('{}/api/v1/users/{}'.format(
            self.host, self.get_user_id()), json=json_obj, headers=self.token)
        if PySenseUtils.response_successful(resp):
            self.reset(json.loads(resp.content))
            return True
        else:
            return None


