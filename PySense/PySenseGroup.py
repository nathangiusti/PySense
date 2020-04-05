import requests

from PySense import PySenseUtils


class Group:

    def __init__(self, host, token, group_json):
        self._host = host
        self._token = token
        self._group_json = group_json

    def get_group_name(self):
        """
        Get groups name  
          
        :return: The name of the group  
        """
        return self._group_json['name']

    def get_group_id(self):
        """
        Get groups id  
          
        :return: The id of the group  
        """
        return self._group_json['_id']

    def add_user_to_group(self, users):
        """
        Adds users to group  
          
        :param users: List of users to add  
        :return: True  
        """
        payload = []
        for user in users:
            payload.append(user.get_user_id())

        resp = requests.post('{}/api/groups/{}/users'.format(self._host, self.get_group_id()),
                             headers=self._token, json=payload)
        PySenseUtils.parse_response(resp)
        return True

    def delete_user_from_group(self, users):
        """
        Remove users from group  
          
        :param users: Users to remove  
        :return: True  
        """
        payload = []
        for user in users:
            payload.append(user.get_user_id())

        resp = requests.post('{}/api/groups/{}/users'.format(self._host, self.get_group_id()),
                             headers=self._token, json=payload)
        PySenseUtils.parse_response(resp)
        return True

