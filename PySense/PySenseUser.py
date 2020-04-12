from PySense import PySenseUtils


class User:

    def __init__(self, connector, user_json):
        self._user_json = user_json
        self._connector = connector

    def _reset(self, user_json):
        self._user_json = user_json

    def get_id(self):
        """
        Returns the user's id  

        :return: The user id  
        """
        
        return self._user_json['_id']
    
    def get_groups(self):
        """
        Returns the groups a user is in
        
        :return: An array of groups 
        """
        ret_arr = []
        for group in self._user_json['groups']:
            ret_arr.append(self._connector.get_group_by_id(group))
        return ret_arr

    def get_email(self):
        """
        Returns the user's email  

        :return: The user's    
        """

        return self._user_json['email']
    
    def get_user_name(self):
        """
        Returns the user's username  
  
        :return: The user's username  
        """
        
        return self._user_json['userName']

    def get_first_name(self):
        """
        Returns the user's first name  
  
        :return: The user's first name  
        """

        return self._user_json['firstName']

    def get_last_name(self):
        """
        Returns the user's last name  

        :return: The user's last name  
        """

        return self._user_json['lastName']
    
    def get_role(self):
        """
        Returns the user's role  

        :return: The user's role  
        """
        
        return self._connector.get_role_name(self._user_json['roleId'])

    def _get_role_id(self):
        return self._user_json['roleId']
    
    def get_preferences(self):
        """
        Get's the user's preferences  
            
        :return: A json blob of preferences  
        """
        return self._user_json['preferences']

    def update(self, *, email=None, user_name=None, first_name=None, last_name=None, role_name=None, groups=None,
               preferences=None):
        """
        Updates given fields for user object. Returns true if successful, None if error   
  
        Optional:
        
        :param email: Value to update email to  
        :param user_name: Value to update username to  
        :param first_name: Value to update firstName to  
        :param last_name: Value to update lastName to  
        :param role_name: New role for user  
        :param groups: New set of groups for user  
        :param preferences: Preferences to be updated for user    
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
                'roleId': self._connector.get_role_id(role_name) if role_name else self._get_role_id(),
                'groups': group_arr,
                'preferences': preferences if preferences else self.get_preferences()
            }
        resp_json = self._connector.rest_call('patch', 'api/v1/users/{}'.format(self.get_id()), json_payload=user_json)
        self._reset(resp_json)
