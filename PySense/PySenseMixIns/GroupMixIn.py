from PySense import PySenseGroup, PySenseUtils


class GroupMixIn:

    def get_groups(self, *, name=None, mail=None, role=None, origin=None, ids=None, fields=None,
                   sort=None, skip=None, limit=None, expand=None):
        """Returns a list of user groups with their details.
        The results can be filtered by different parameters such as group name or origin.

        Args:
            name: (optional) Group name to filter by
            mail: (optional) Group email to filter by
            role: (optional) Group role to filter by
            origin: (optional) Group origin to filter by (ad or sisense)
            ids: (optional) Array of group IDs to filter by
            fields: (optional) Whitelist of fields to return for each document.
                Fields can also define which fields to exclude by prefixing field names with -
            sort: (optional) Field by which the results should be sorted.
                Ascending by default, descending if prefixed by -
            skip: (optional) Number of results to skip from the start of the data set.
                Skip is to be used with the limit parameter for paging
            limit: (optional) How many results should be returned.
                limit is to be used with the skip parameter for paging
            expand: (optional) List of fields that should be expanded (substitures their IDs with actual objects).
                May be nested using the resource.subResource format

        Returns:
            Array of found groups
        """

        query_params = {
            'name': name,
            'mail': mail,
            'roleId': self.get_role_id(role),
            'origin': origin,
            'ids': ids,
            'fields': fields,
            'sort': sort,
            'skip': skip,
            'limit': limit,
            'expand': expand
        }
        resp_json = self.connector.rest_call('get', 'api/v1/groups', query_params=query_params)

        ret_arr = []
        for group in resp_json:
            ret_arr.append(PySenseGroup.Group(self, group))
        return ret_arr


    def get_group_by_id(self, group_id):
        """Get a group by id"""
        if group_id is None:
            return None
        resp_json = self.connector.rest_call('get', 'api/groups/{}'.format(group_id))
        return PySenseGroup.Group(self, resp_json)


    def get_groups_by_name(self, group_names):
        """Returns an array of groups matching the given names

        Args:
            group_names: One to many group names
        """
        if group_names is None:
            return []

        server_groups = self.get_groups()
        ret = []
        group_names = PySenseUtils.make_iterable(group_names)
        for group in server_groups:
            if group.get_name() in group_names:
                ret.append(group)
        return ret

    def add_groups(self, names):
        """Add groups with given names.

        Args:
            names: One to many names

        Returns:
            Array of new groups
        """
        ret_arr = []
        for name in PySenseUtils.make_iterable(names):
            payload = {'name': name}
            resp_json = self.connector.rest_call('post', 'api/v1/groups', json_payload=payload)
            ret_arr.append(PySenseGroup.Group(self, resp_json))
        return ret_arr

    def delete_groups(self, groups):
        """Delete groups.

        Args:
            groups: One to many groups to delete
        """
        for group in PySenseUtils.make_iterable(groups):
            self.connector.rest_call('delete', 'api/groups/{}'.format(group.get_id()))
