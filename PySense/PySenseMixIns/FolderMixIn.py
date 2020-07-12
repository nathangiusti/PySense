from PySense import PySenseFolder


class FolderMixIn:

    def get_folders(self, *, name=None, structure=None, ids=None, fields=None,
                    sort=None, skip=None, limit=None, expand=None):
        """Provides access to a specified user’s folders in their stored format.

        Args:
            name: (optional) Name to filter by
            structure: (optional) Structure type of the folders
            ids: (optional) Array of folder IDs to get, separated by a comma (,) and without spaces
            fields: (optional) Whitelist of fields to return for each document.
                Fields Can also define which fields to exclude by prefixing field names with -
            sort: (optional) Field by which the results should be sorted.
                Ascending by default, descending if prefixed by -
            skip: (optional) Number of results to skip from the start of the data set.
                Skip is to be used with the limit parameter for paging
            limit: (optional) How many results should be returned.
                limit is to be used with the skip parameter for paging
            expand: (optional) List of fields that should be expanded (substitue their IDs with actual objects).
                May be nested using the resource.subResource format

        Returns:
             An array of folders matching the search criteria
        """
        ret_arr = []
        query_params = {
            'name': name,
            'structure': structure,
            'ids': ids,
            'fields': fields,
            'sort': sort,
            'skip': skip,
            'limit': limit,
            'expand': expand
        }

        resp_json = self.connector.rest_call('get', 'api/v1/folders', query_params=query_params)

        # Sisense Rest API always returns the root folder, so we filter it out when looking by name
        if name:
            for folder in resp_json:
                if folder['name'] == name:
                    ret_arr.append(PySenseFolder.Folder(self, folder))
        else:
            for folder in resp_json:
                ret_arr.append(PySenseFolder.Folder(self, folder))
        return ret_arr

    def get_folder_by_id(self, folder_id):
        """Get a specific folder by folder id."""
        if folder_id is None:
            return None
        resp_json = self.connector.rest_call('get', 'api/v1/folders/{}'.format(folder_id))
        return PySenseFolder.Folder(self, resp_json)