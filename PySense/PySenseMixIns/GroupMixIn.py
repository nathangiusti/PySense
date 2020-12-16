from PySense import PySenseGroup, PySenseUtils


class GroupMixIn:

    def get_groups(self, *, name=None, mail=None, role=None, origin=None, ids=None, fields=None,
                   sort=None, skip=None, limit=None, expand=None):
        """Returns a list of user groups with their details.
        The results can be filtered by different parameters such as group name or origin.

        Args:
            name (str): (Optional) Group name to filter by
            mail (str): (Optional) Group email to filter by
            role (str): (Optional) Group role to filter by
            origin (str): (Optional) Group origin to filter by (ad or sisense)
            ids (list[str]): (Optional) Array of group IDs to filter by
            fields (list[str]): (Optional) Whitelist of fields to return for each document.
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
            list[Group]: The found groups
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
        """Get a group by id

        Args:
            group_id (str): The id of the group to look for

        Returns:
            Group: The group with the given id
        """

        if group_id is None:
            return None
        resp_json = self.connector.rest_call('get', 'api/groups/{}'.format(group_id))
        return PySenseGroup.Group(self, resp_json)

    def get_groups_by_name(self, group_names):
        """Returns an array of groups matching the given names

        Args:
            group_names (list[str]): Group names to look for

        Returns:
            list[Group]: Groups with the given names
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
            names (str): The names of the new groups

        Returns:
            list[Group]: The new groups
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
            groups (list[Group]): Groups to delete
        """

        for group in PySenseUtils.make_iterable(groups):
            self.connector.rest_call('delete', 'api/groups/{}'.format(group.get_id()))
