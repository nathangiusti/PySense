from PySense import PySenseUtils


class User:

    def __init__(self, py_client, user_json):
        self._user_json = user_json
        self._py_client = py_client

    def _reset(self, user_json):
        self._user_json = user_json

    def get_id(self):
        """Returns the user's id."""
        return self._user_json['_id']
    
    def get_groups(self):
        """Returns the groups a user is in."""
        ret_arr = []
        for group in self._user_json['groups']:
            ret_arr.append(self._py_client.get_group_by_id(group))
        return ret_arr

    def get_email(self):
        """Returns the user's email"""
        return self._user_json['email']
    
    def get_user_name(self):
        """Returns the user's username."""
        return self._user_json['userName']

    def get_first_name(self):
        """Returns the user's first name."""
        return self._user_json['firstName']

    def get_last_name(self):
        """Returns the user's last name."""

        return self._user_json['lastName']
    
    def get_last_login(self):
        """Returns the time the user last logged in."""
        return PySenseUtils.sisense_time_to_python(self._user_json['lastLogin'])
    
    def get_role(self):
        """Returns the user's role."""
        return self._py_client.get_role_name(self._user_json['roleId'])

    def get_role_id(self):
        """Returns the role id."""
        return self._user_json['roleId']
    
    def get_preferences(self):
        """Get's the user's preferences."""
        return self._user_json['preferences']

    def update(self, *, email=None, user_name=None, first_name=None, last_name=None, role_name=None, groups=None,
               preferences=None):
        """Updates given fields for user object.  
  
        Optional:
            - email: Value to update email to  
            - user_name: Value to update username to  
            - first_name: Value to update firstName to  
            - last_name: Value to update lastName to  
            - role_name: New role for user  
            - groups: New set of groups for user  
            - preferences: Preferences to be updated for user    
        """ 
        user_groups = groups if groups is not None else self.get_groups()
        group_arr = []
        for group in PySenseUtils.make_iterable(user_groups):
            group_arr.append(group.get_id())
            
        user_json = {
                'email': email if email else self.get_email(),
                'userName': user_name if user_name else self.get_user_name(),
                'firstName': first_name if first_name else self.get_first_name(),
                'lastName': last_name if last_name else self.get_last_name(),
                'roleId': self._py_client.get_role_id(role_name) if role_name else self.get_role_id(),
                'groups': group_arr,
                'preferences': preferences if preferences else self.get_preferences()
            }
        resp_json = self._py_client.connector.rest_call('patch', 'api/v1/users/{}'.format(self.get_id()), json_payload=user_json)
        self._reset(resp_json)
