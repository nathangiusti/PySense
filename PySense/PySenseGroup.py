from PySense import PySenseUtils


class Group:

    def __init__(self, py_client, group_json):
        self._py_client = py_client
        self._group_json = group_json

    def get_name(self):
        """Get groups name"""
        return self._group_json['name']

    def get_id(self):
        """Get groups id."""

        return self._group_json['_id']

    def get_users(self):
        """Returns the members of the group."""
        resp_json = self._py_client.connector.rest_call('get', 'api/groups/{}/users'.format(self.get_id()))
        ret_arr = []
        for user in resp_json:
            ret_arr.append(self._py_client.get_user_by_email(user['email']))
        return ret_arr

    def add_user(self, users):
        """Adds users to group."""
        payload = []
        for user in PySenseUtils.make_iterable(users):
            payload.append(user.get_id())

        self._py_client.connector.rest_call('post', 'api/groups/{}/users'.format(self.get_id()), json_payload=payload)

    def remove_user(self, users):
        """Remove users from group"""
        payload = []
        for user in PySenseUtils.make_iterable(users):
            payload.append(user.get_id())

        self._py_client.connector.rest_call('delete', 'api/groups/{}/users'.format(self.get_id()), json_payload=payload)
