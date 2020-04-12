from PySense import PySenseUtils


class Group:

    def __init__(self, connector, group_json):
        self._connector = connector
        self._group_json = group_json

    def get_name(self):
        """
        Get groups name  
          
        :return: The name of the group  
        """
        
        return self._group_json['name']

    def get_id(self):
        """
        Get groups id  
          
        :return: The id of the group  
        """
        
        return self._group_json['_id']
    
    def get_users(self):
        """
        Returns the members of the group  
          
        :return:  An array of PySense Users 
        """
        resp_json = self._connector.rest_call('get', 'api/groups/{}/users'.format(self.get_id()))
        ret_arr = []
        for user in resp_json:
            ret_arr.append(self._connector.get_user_by_email(user['email']))
        return ret_arr

    def add_user(self, users):
        """
        Adds users to group  
          
        :param users: One to many users to add 
        """
        
        payload = []
        for user in PySenseUtils.make_iterable(users):
            payload.append(user.get_id())

        self._connector.rest_call('post', 'api/groups/{}/users'.format(self.get_id()), json_payload=payload)

    def remove_user(self, users):
        """
        Remove users from group  
          
        :param users: One to many users to remove from group   
        """
        
        payload = []
        for user in PySenseUtils.make_iterable(users):
            payload.append(user.get_id())
            
        self._connector.rest_call('delete', 'api/groups/{}/users'.format(self.get_id()), json_payload=payload)
