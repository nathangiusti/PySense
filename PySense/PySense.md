Module PySense.PySense
======================

Functions
---------

    
`authenticate_by_file(config_file)`
:   Creates a new PySense client with the credentials in the given config file.
    
    :param config_file: Yaml file with entries for host, username, and password
    :return: A new PySense client for the given credentials

Classes
-------

`PySense(host, username, password)`
:   

    ### Methods

    `add_groups(self, name_array)`
    :   Add group with given name
        @param name_array: Array of new group names
        @return: Array of new groups

    `add_user(self, email, username, role, *, first_name=None, last_name=None, groups=None, preferences=None, ui_settings=None)`
    :   Creates that user in SiSense, returning the created object.
        If a user with the same username or email exists, it will return an error.
        
        @param email: email address for user
        @param username: username
        @param role: role name
        @param first_name: user first name
        @param last_name: user last name
        @param groups: The groups to add the user to
        @param preferences: User preferences
        @param ui_settings: User ui settings
        @return: Newly created user object

    `custom_rest(self, action_type, url, *, data=None, json_payload=None)`
    :   Run an arbitrary rest command against your Sisense instance.
        
        :param action_type: REST request type
        :param url: url to hit, example api/v1/app_database/encrypt_database_password or api/branding
        :param data: The data portion of the payload
        :param json_payload: The json portion of the payload
        :return: The rest response object

    `delete_dashboards(self, dashboard_id)`
    :   Delete dashboard with id
        
        :param dashboard_id: The ID of the dashboard to delete
        :return: The response object

    `delete_groups(self, group_array)`
    :   Add group with given name
        @param group_array: Array of groups to delete
        @return: The new group

    `delete_user(self, user)`
    :   Deletes the specified user
        @param user: User obj to delete
        @return: Response

    `get_authentication(self)`
    :   Returns authentication parameters
        @return: A dictionary with an entry for host and token

    `get_dashboard_by_id(self, dashboard_id, *, fields=None, expand=None)`
    :   Returns a specific dashboard object by ID.
        
        :param dashboard_id: The ID of the dashboard to get
        :param fields: Whitelist of fields to return for each document. fields Can also define which fields to exclude
            by prefixing field names with -
        :param expand: List of fields that should be expanded (substitures their IDs with actual objects). May be nested
            using the resource.subResource format
        :return: Dashboard with id given

    `get_dashboards(self, *, parent_folder_name=None, name=None, data_source_title=None, data_source_address=None, fields=None, sort=None, expand=None)`
    :   Get all dashboards
        
        :param parent_folder_name: Parent folder name to filter by
        :param name: Name to filter by
        :param data_source_title: Data source name to filter by
        :param data_source_address: Data source address to filter by
        :param fields: Whitelist of fields to return for each document.
           Can also exclude by prefixing field names with -
        :param sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -
        :param expand: List of fields that should be expanded
        :return: All found dashboards

    `get_elasticube_by_name(self, name)`
    :   Gets elasticube by name
        
        :param name: Name of elasticube to get
        :return: An array of elasticubes matching the query

    `get_elasticubes(self)`
    :   Gets elasticubes
        :return: An array of elasticubes

    `get_folder_by_id(self, folder_id)`
    :   Get a specific folder by folder id
        
        @param folder_id: The folder id of the folder
        @return: A PySense folder object of the folder

    `get_folders(self, *, name=None, structure=None, ids=None, fields=None, sort=None, skip=None, limit=None, expand=None)`
    :   Provides access to a specified user’s folders in their stored format
        
        @param name: Name to filter by
        @param structure: Structure type of the folders
        @param ids: Array of folder IDs to get, separated by a comma (,) and without spaces
        @param fields: Whitelist of fields to return for each document. fields Can also define which fields to exclude
            by prefixing field names with -
        @param sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -
        @param skip: Number of results to skip from the start of the data set. skip is to be used with the limit
            parameter for paging
        @param limit: How many results should be returned. limit is to be used with the skip parameter for paging
        @param expand: List of fields that should be expanded (substitures their IDs with actual objects). May be
            nested using the resource.subResource format
        @return: An array of folders matching the search criteria

    `get_group_ids(self, groups)`
    :   Get the ids for groups
        @param groups: An array of group names
        @return: An array of ids for the groups

    `get_groups(self, *, name=None, mail=None, role=None, origin=None, ids=None, fields=None, sort=None, skip=None, limit=None, expand=None)`
    :   Returns a list of user groups with their details.
        The results can be filtered by different parameters such as group name or origin.
        
        :param name: Group name to filter by
        :param mail: Group email to filter by
        :param role: Group role to filter by
        :param origin: Group origin to filter by (ad or sisense)
        :param ids: Array of group IDs to filter by
        :param fields: Whitelist of fields to return for each document.
            Fields can also define which fields to exclude by prefixing field names with -
        :param sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -
        :param skip: Number of results to skip from the start of the data set.
            Skip is to be used with the limit parameter for paging
        :param limit: How many results should be returned. limit is to be used with the skip parameter for paging
        :param expand: List of fields that should be expanded (substitures their IDs with actual objects).
            May be nested using the resource.subResource format
        :return: Array of found groups

    `get_users(self, *, user_name=None, email=None, first_name=None, last_name=None, role_name=None, group=None, active=None, origin=None, ids=None, fields=None, sort=None, skip=None, limit=None, expand=None)`
    :   Returns a list of users with their details.
        Results can be filtered by parameters such as username and email.
        The expandable fields for the user object are groups, adgroups and role.
        
        @param user_name: Username to filter by
        @param email: Email to filter by
        @param first_name: First name to filter by
        @param last_name: Last name to filter by
        @param role_name: Role filter by
        @param group: Group to filter by
        @param active: User state to filter by (true for active users, false for inactive users)
        @param origin: User origin to filter by (ad for active directory or sisense)
        @param ids: Array of user ids to get separated by comma and without spaces
        @param fields: Whitelist of fields to return for each document.
            Fields can also define which fields to exclude by prefixing field names with -
        @param sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -
        @param skip: Number of results to skip from the start of the data set.
            Skip is to be used with the limit parameter for paging
        @param limit: How many results should be returned. limit is to be used with the skip parameter for paging
        @param expand: List of fields that should be expanded (substitutes their IDs with actual objects).
            May be nested using the resource.subResource format
        
        @return: An array of users objects

    `post_alert(self, alert_obj)`
    :

    `post_dashboards(self, dashboard_json)`
    :   Import given dashboard
        
        :param dashboard_json: The dashboard json from the dash file
        :return: The dashboard given by the response object