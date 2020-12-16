from PySense import PySenseUtils


class Group:
    """A group of users

    Groups contain 0 to many users

    Attributes:
        json (JSON): The JSON for this object
        py_client (PySense): The connection to the Sisense server which owns this asset
    """

    def __init__(self, py_client, group_json):
        """

        Args:
            py_client (PySense): The PySense object for the server this asset belongs to
            group_json (JSON): The json for this object
        """

        self.py_client = py_client
        self.json = group_json

    def get_name(self):
        """Get groups name"""

        return self.json['name']

    def get_id(self):
        """Get groups id."""

        return self.json['_id']

    def get_users(self):
        """Returns the members of the group.

        Returns:
            list[User]: The users in the group
        """

        resp_json = self.py_client.connector.rest_call('get', 'api/groups/{}/users'.format(self.get_id()))
        ret_arr = []
        for user in resp_json:
            ret_arr.append(self.py_client.get_user_by_email(user['email']))
        return ret_arr

    def add_user(self, users):
        """Adds users to group.

        Args:
            users (list[User]): The users to add to the group
        """

        payload = []
        for user in PySenseUtils.make_iterable(users):
            payload.append(user.get_id())

        self.py_client.connector.rest_call('post', 'api/groups/{}/users'.format(self.get_id()), json_payload=payload)

    def remove_user(self, users):
        """Remove users from group

        Args:
            users (list[User]): Users to remove from the group
        """

        payload = []
        for user in PySenseUtils.make_iterable(users):
            payload.append(user.get_id())

        self.py_client.connector.rest_call('delete', 'api/groups/{}/users'.format(self.get_id()), json_payload=payload)
