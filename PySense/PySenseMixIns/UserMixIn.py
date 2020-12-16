from PySense import PySenseException, PySenseUser, PySenseUtils


class UserMixIn:

    def add_user(self, email, role, *, user_name=None, first_name=None, last_name=None,
                 groups=[], preferences={}, ui_settings={}, password=None):
        """Creates a user in Sisense.

        Args:
            email (str): email address for user
            role (Role): SisenseRole enum for the role of the user
            user_name (str): (Optional) User user name. Email used if None
            first_name (str): (Optional) User first name
            last_name (str): (Optional) User last name
            groups (str): (Optional) The groups to add the user to
            preferences (str): (Optional) User preferences
            ui_settings (JSON): (Optional) User ui settings
            password (str): (Optional) The password to set for the user

        Returns:
             User: Newly created user object
        """

        user_obj = {
            'email': email,
            'username': user_name if user_name is not None else email,
            'roleId': self.get_role_id(role)
        }

        group_ids = []
        for group in PySenseUtils.make_iterable(groups):
            group_ids.append(group.get_id())
        if len(group_ids) > 0:
            user_obj['groups'] = group_ids

        if first_name is not None:
            user_obj['firstName'] = first_name
        if last_name is not None:
            user_obj['lastName'] = last_name
        if preferences is not None:
            user_obj['preferences'] = preferences
        if ui_settings is not None:
            user_obj['uiSettings'] = ui_settings
        if password is not None:
            user_obj['password'] = password

        resp_json = self.connector.rest_call('post', 'api/v1/users', json_payload=user_obj)
        return PySenseUser.User(self, resp_json)

    def get_users(self, *, user_name=None, email=None, first_name=None, last_name=None, role=None, group=None,
                  active=None, origin=None, ids=None, fields=[], sort=None, skip=None, limit=None, expand=None):
        """Returns a list of users.

        Results can be filtered by parameters such as username and email.
        The expandable fields for the user object are groups, adgroups and role.

        Args:
            user_name (str): (Optional) Username to filter by
            email (str): (Optional) Email to filter by
            first_name (str): (Optional) First name to filter by
            last_name (str): (Optional) Last name to filter by
            role (Role): (Optional) SisenseRole enum for the role of the user to filter by
            group (Group): (Optional) Group to filter by
            active (bool): (Optional) User state to filter by (true for active users, false for inactive users)
            origin (str): (Optional) User origin to filter by (ad for active directory or sisense)
            ids (list[str]): (Optional) User ids to get
            fields (list[str]): (Optional) An array of fields to return for each document.
                Fields can also define which fields to exclude by prefixing field names with -
            sort (str): (Optional) Field by which the results should be sorted.
                Ascending by default, descending if prefixed by -
            skip (int): (Optional) Number of results to skip from the start of the data set.
                Skip is to be used with the limit parameter for paging
            limit (int): (Optional) How many results should be returned.
                limit is to be used with the skip parameter for paging
            expand (list[str]): (Optional) List of fields that should be expanded
                May be nested using the resource.subResource format

        Returns:
             list[User]: Users found
        """

        fields = PySenseUtils.make_iterable(fields)

        # Ensure we get the fields we need to manage the user even if fields is set
        fields.extend(
            ['_id', 'lastLogin', 'groups', 'email', 'userName', 'firstName', 'lastName', 'roleId', 'preferences']
        )

        fields = list(dict.fromkeys(fields))
        query_params = {
            'userName': user_name,
            'email': email,
            'firstName': first_name,
            'lastName': last_name,
            'role': self.get_role_id(role),
            'group': None if group is None else group.get_id(),
            'active': active,
            'origin': origin,
            'ids': ids,
            'fields': fields,
            'sort': sort,
            'skip': skip,
            'limit': limit,
            'expand': expand
        }
        ret_arr = []
        resp_json = self.connector.rest_call('get', 'api/v1/users', query_params=query_params)
        for user in resp_json:
            ret_arr.append((PySenseUser.User(self, user)))
        return ret_arr

    def get_user_by_email(self, email):
        """Returns a single user based on email

        Args:
            email (str): The email of the user to get

        Returns:
            User: The user with the email address
        """
        users = self.get_users(email=email)
        if len(users) == 0:
            None
        elif len(users) > 1:
            raise PySenseException.PySenseException('{} users with email {} found. '.format(len(users), email))
        else:
            return users[0]

    def get_user_by_id(self, user_id):
        """Returns a single user based on id

        Args:
            user_id (str): The user_id of the user to fetch

        Returns:
            User: The user with the given id
        """

        resp_json = self.connector.rest_call('get', 'api/v1/users/{}'.format(user_id))
        return PySenseUser.User(self, resp_json)

    def delete_users(self, users):
        """Deletes the specified users

        Args:
            users: Users to delete
        """

        for user in PySenseUtils.make_iterable(users):
            self.connector.rest_call('delete', 'api/v1/users/{}'.format(user.get_id()))

    def add_users_active_directory(self, users):
        """Adds users from active directory

        Beta: May have issues

        Args:
            users (JSON): A json array of active directory user blobs

        Ex:
        [
          {
            "userName": "string",
            "ldapDomainId": "string",
            "roleId": "string",
            "groups": [
              "string"
            ],
            "objectSid": "string",
            "preferences": {
              "localeId": "Unknown Type: string,null"
            },
            "uiSettings": {}
          }
        ]

        Returns:
             JSON: the JSON response
        """

        return self.connector.rest_call('post', 'api/v1/users/ad/bulk', json_payload=users)



