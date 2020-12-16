from PySense import PySenseUtils


class User:
    """A user on the server

    Attributes:
        json (JSON): The JSON for this object
        py_client (PySense): The connection to the Sisense server which owns this asset
    """

    def __init__(self, py_client, user_json):
        """
        Args:
            py_client (PySense): The PySense object for the server this asset belongs to
            user_json (JSON): The json for this object
        """
        self.json = user_json
        self.py_client = py_client

    def _reset(self, user_json):
        self.json = user_json

    def get_id(self):
        """Returns the user's id."""

        return self.json['_id']

    def get_groups(self):
        """Returns the groups a user is in

        Returns:
            list[Group]: Groups the user is a member of
        """

        ret_arr = []
        if 'groups' not in self.json:
            return []
        for group in self.json['groups']:
            ret_arr.append(self.py_client.get_group_by_id(group))
        return ret_arr

    def get_email(self):
        """Returns the user's email"""

        if 'email' in self.json:
            return self.json['email']
        else:
            return ""

    def get_user_name(self):
        """Returns the user's username."""

        if 'userName' in self.json:
            return self.json['userName']
        else:
            return ""

    def get_first_name(self):
        """Returns the user's first name."""

        if 'firstName' in self.json:
            return self.json['firstName']
        else:
            return ""

    def get_last_name(self):
        """Returns the user's last name."""

        if 'lastName' in self.json:
            return self.json['lastName']
        else:
            return ""

    def get_last_login(self):
        """Returns the time the user last logged in.

        Returns:
            datetime: The datetime the user last logged in
        """

        return PySenseUtils.sisense_time_to_python(self.json['lastLogin'])

    def get_role(self):
        """Returns the user's role.

        Returns:
            Role: The role assigned to this user
        """

        return self.py_client.get_role_by_id(self.json['roleId'])

    def get_role_id(self):
        """Returns the role id."""

        return self.json['roleId']

    def get_preferences(self):
        """Get's the user's preferences."""

        return self.json['preferences']

    def update(self, *, email=None, user_name=None, first_name=None, last_name=None, role=None, groups=None,
               preferences=None):
        """Updates given fields for user object.

        Args:
            email (str): (Optional) Value to update email to
            user_name (str): (Optional) Value to update username to
            first_name (str): (Optional) Value to update firstName to
            last_name (str): (Optional) Value to update lastName to
            role (Role): (Optional) New role for user
            groups (list[Group]): (Optional) New set of groups for user
            preferences (JSON): (Optional) Preferences to be updated for user
        """

        user_groups = groups if groups is not None else self.get_groups()
        group_arr = []
        for group in PySenseUtils.make_iterable(user_groups):
            group_arr.append(group.get_oid())

        user_json = {
                'email': email if email else self.get_email(),
                'userName': user_name if user_name else self.get_user_name(),
                'firstName': first_name if first_name else self.get_first_name(),
                'lastName': last_name if last_name else self.get_last_name(),
                'roleId': self.py_client.get_role_id(role) if role else self.get_role_id(),
                'groups': group_arr,
                'preferences': preferences if preferences else self.get_preferences()
            }
        resp_json = self.py_client.connector.rest_call('patch', 'api/v1/users/{}'.format(self.get_id()),
                                                       json_payload=user_json)
        self._reset(resp_json)

    def change_password(self, new_password):
        """ Change user's password

        Args:
            new_password (str): The new password for the user
        """

        user_json = self.json
        user_json['password'] = new_password
        self.py_client.connector.rest_call('put', 'api/users/{}'.format(self.get_id()), json_payload=user_json)

