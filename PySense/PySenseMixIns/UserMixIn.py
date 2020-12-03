from PySense import PySenseException, PySenseUser, PySenseUtils


class UserMixIn:

    def add_user(self, email, role, *, user_name=None, first_name=None, last_name=None,
                 groups=[], preferences={}, ui_settings={}):
        """Creates a user in Sisense.

        Args:
            email: email address for user
            role: SisenseRole enum for the role of the user
            user_name: (optional) User user name. Email used if None
            first_name: (optional) User first name
            last_name: (optional) User last name
            groups: (optional) The groups to add the user to
            preferences: (optional) User preferences
            ui_settings: (optional) User ui settings

        Returns:
             Newly created user object
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

        resp_json = self.connector.rest_call('post', 'api/v1/users', json_payload=user_obj)
        return PySenseUser.User(self, resp_json)

    def get_users(self, *, user_name=None, email=None, first_name=None, last_name=None, role=None, group=None,
                  active=None, origin=None, ids=None, fields=[], sort=None, skip=None, limit=None, expand=None):
        """Returns a list of users.

        Results can be filtered by parameters such as username and email.
        The expandable fields for the user object are groups, adgroups and role.

        Args:
            user_name: (optional) Username to filter by
            email: (optional) Email to filter by
            first_name: (optional) First name to filter by
            last_name: (optional) Last name to filter by
            role: (optional) SisenseRole enum for the role of the user to filter by
            group: (optional) Group to filter by
            active: (optional) User state to filter by (true for active users, false for inactive users)
            origin: (optional) User origin to filter by (ad for active directory or sisense)
            ids: (optional) Array of user ids to get
            fields: (optional) An array of fields to return for each document.
                Fields can also define which fields to exclude by prefixing field names with -
            sort: (optional) Field by which the results should be sorted.
                Ascending by default, descending if prefixed by -
            skip: (optional) Number of results to skip from the start of the data set.
                Skip is to be used with the limit parameter for paging
            limit: (optional) How many results should be returned.
                limit is to be used with the skip parameter for paging
            expand: (optional) List of fields that should be expanded (substitutes their IDs with actual objects).
                May be nested using the resource.subResource format

        Returns:
             An array of PySenseUser.User objects
        """

        fields = PySenseUtils.make_iterable(fields)
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
            'group': group,
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
        """Returns a single user based on email"""
        users = self.get_users(email=email)
        if len(users) == 0:
            None
        elif len(users) > 1:
            raise PySenseException.PySenseException('{} users with email {} found. '.format(len(users), email))
        else:
            return users[0]

    def get_user_by_id(self, user_id):
        """Returns a single user based on id"""
        resp_json = self.connector.rest_call('get', 'api/v1/users/{}'.format(user_id))
        return PySenseUser.User(self, resp_json)

    def delete_users(self, users):
        """Deletes the specified user or users

        Args:
            users: One to many users to delete
        """
        for user in PySenseUtils.make_iterable(users):
            self.connector.rest_call('delete', 'api/v1/users/{}'.format(user.get_id()))

    def add_users_active_directory(self, users):
        """Adds users from active directory

        Beta: May have issues

        Args:
            users: A json array of active directory user blobs

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

        Returns the JSON response
        """

        return self.connector.rest_call('post', 'api/v1/users/ad/bulk', json_payload=users)



