from PySense import PySenseFolder, PySenseUtils


class FolderMixIn:

    def get_folders(self, *, name=None, structure=None, ids=None, fields=None,
                    sort=None, skip=None, limit=None, expand=None):
        """Provides access to a specified user’s folders in their stored format.

        Args:
            name (str): (optional) Name to filter by
            structure (str): (optional) Structure type of the folders
            ids (list[str]): (optional) List of folder IDs to get
            fields (list[str]): (optional) Whitelist of fields to return for each document.
                Fields Can also define which fields to exclude by prefixing field names with -
            sort (str): (optional) Field by which the results should be sorted.
                Ascending by default, descending if prefixed by -
            skip (int): (optional) Number of results to skip from the start of the data set.
                Skip is to be used with the limit parameter for paging
            limit (int): (optional) How many results should be returned.
                limit is to be used with the skip parameter for paging
            expand (list[str]): (optional) List of fields that should be expanded
                May be nested using the resource.subResource format

        Returns:
             list[Folder]: An array of folders matching the search criteria
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
        """Get a specific folder by folder id.

        Args:
            folder_id (str): The folder id to look for

        Returns:
            Folder: The folder with the given id
        """

        if folder_id is None:
            return None
        resp_json = self.connector.rest_call('get', 'api/v1/folders/{}'.format(folder_id))
        return PySenseFolder.Folder(self, resp_json)

    def add_folder(self, name, *, parent_folder=None):
        """Add a folder

        Args:
            name (str): Name of the new folder
            parent_folder (Folder): (Optional) The parent folder to create this within

        Returns:
            Folder: The new folder
        """
        if parent_folder is not None:
            payload = {"name": name, "parentId": parent_folder.get_oid()}
        else:
            payload = {"name": name}

        resp_json = self.connector.rest_call('post', 'api/v1/folders', json_payload=payload)
        return PySenseFolder.Folder(self, resp_json)

    def delete_folders(self, folders):
        """Delete given folders

        Args:
            folders (list[Folder]): Folders to delete
        """

        folder_arr = []
        for folder in PySenseUtils.make_iterable(folders):
            folder_arr.append(folder.get_oid())

        query_params = {
            "folderIds": ','.join(folder_arr)
        }
        self.connector.rest_call('delete', 'api/v1/folders/bulk', query_params=query_params)
