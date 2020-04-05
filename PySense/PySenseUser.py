import json
import requests

from PySense import PySenseUtils


class User:

    def __init__(self, host, token, user_json):
        self._host = host
        self._token = token
        self._user_json = user_json

    def _reset(self, user_json):
        self._user_json = user_json

    def get_user_id(self):
        """
        Returns the user's id  

        :return: The user id  
        """
        return self._user_json['_id']

    def get_user_user_name(self):
        """
        Returns the user's username  
  
        :return: The user's    
        """
        return self._user_json['userName']

    def update_user(self, *, email=None, user_name=None, first_name=None, last_name=None, role_name=None, groups=None,
                    preferences=None, ui_settings=None):
        """
        Updates given fields for user object. Returns true if successful, None if error   
  
        :param email: Value to update email to  
        :param user_name: Value to update username to  
        :param first_name: Value to update firstName to  
        :param last_name: Value to update lastName to  
        :param role_name: New role for user  
        :param groups: Groups to put user in  
        :param preferences: Preferences to be updated for user  
        :param ui_settings: UI Settings to be updated for user  
        :return: True if successful  
        """  

        json_obj = PySenseUtils.build_json_object(
            {
                'email': email,
                'userName': user_name,
                'firstName': first_name,
                'lastName': last_name,
                'role': PySenseUtils.get_role_id(self._host, self._token, role_name),
                'groups': groups,
                'preferences': preferences,
                'uiSettings': ui_settings
            }
        )
        resp = requests.patch('{}/api/v1/users/{}'.format(
            self._host, self.get_user_id()), json=json_obj, headers=self._token)
        PySenseUtils.parse_response(resp)
        self._reset(json.loads(resp.content))
        return True
