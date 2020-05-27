import yaml

from PySense import PySenseConnection
from PySense import PySenseDashboard
from PySense import PySenseDataModel
from PySense import PySenseElasticube
from PySense import PySenseException
from PySense import PySenseGroup
from PySense import PySenseFolder
from PySense import PySensePlugin
from PySense import PySenseRestConnector
from PySense import PySenseUser
from PySense import PySenseUtils
from PySense import SisenseVersion


def authenticate_by_file(config_file):
    """Creates a new PySense client with the credentials in the given config file.

    py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')

    Sample yaml
    host: 'your_host'
    username: 'your_username@sample.com'
    password: 'your_password'
    version: 'your platform'

    Args:
        config_file: Yaml file with entries for host, username, and password

    Returns:
        A new PySense client for the given credentials
    """

    with open(config_file, 'r') as yml_file:
        cfg = yaml.safe_load(yml_file)

        debug = cfg['debug'] if 'debug' in cfg else False
        verify = cfg['verify'] if 'verify' in cfg else True

        return PySense(cfg['host'], cfg['username'], cfg['password'], cfg['version'], debug=debug, verify=verify)


class PySense:
    """The manager of connections to the PySense server

    This class is for sever level changes like getting, adding, and removing dashboards, elasticubes, users, etc

    Attributes:
        connector: The PySenseRestConnector which runs the rest command.
    """

    def __init__(self, host, username, password, version, *, debug=False, verify=True):
        """ Initializes a PySense instance

        Args:
            host: host address
            username: username
            password: password
            version: version (either 'Windows' or 'Linux')
            debug: If true, prints detailed REST API logs to console. False by default.
            verify: If false, disables SSL Certification. True by default.
        """
        if version.lower() == 'windows':
            self.version = SisenseVersion.Version.WINDOWS
        elif version.lower() == 'linux':
            self.version = SisenseVersion.Version.LINUX
        else:
            raise PySenseException.PySenseException('{} not a valid OS. Please select Linux or Windows'.format(version))

        self.connector = PySenseRestConnector.RestConnector(host, username, password, debug, verify)
        self._roles = self.connector.rest_call('get', 'api/roles')

    def set_debug(self, debug):
        """Enable or disable logging of REST api calls to std out.

        Use for debugging. Debug is false by default.
        """
        self.connector.debug = debug

    ############################################
    # Dashboards                               #
    ############################################

    def get_dashboards(self, *, parent_folder=None, name=None, data_source_title=None,
                       data_source_address=None, fields=None, sort=None, expand=None):
        """Get all dashboards.

        Args:
            parent_folder: Parent folder to filter by
            name: Name to filter by
            data_source_title: Data source name to filter by
            data_source_address: Data source address to filter by
            fields: Whitelist of fields to return for each document.
               Can also exclude by prefixing field names with -
            sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -
            expand: List of fields that should be expanded

        Returns:
            An array of all found dashboards
        """

        folder_id = None
        if parent_folder:
            folder_id = parent_folder.get_id()

        query_params = {
            'parentFolder': folder_id,
            'name': name,
            'datasourceTitle': data_source_title,
            'datasourceAddress': data_source_address,
            'fields': fields,
            'sort': sort,
            'expand': expand
        }
        json_arr = self.connector.rest_call('get', 'api/v1/dashboards', query_params=query_params)

        ret_arr = []
        for dash in json_arr:
            ret_arr.append(PySenseDashboard.Dashboard(self, dash))
        return ret_arr

    def get_dashboard_by_id(self, dashboard_id, *, fields=None, expand=None):
        """Returns a specific dashboard object by ID.

        Args:
            dashboard_id: The ID of the dashboard to get
            fields: (optional) Whitelist of fields to return for each document.
                Fields Can also define which fields to exclude by prefixing field names with -
            expand: (optional) List of fields that should be expanded (substitues their IDs with actual objects).
                May be nested using the resource.subResource format

        Returns:
             Dashboard with the given id.
        """

        query_params = {
            'fields': fields,
            'expand': expand
        }

        resp_json = self.connector.rest_call('get', 'api/v1/dashboards/{}'.format(dashboard_id),
                                             query_params=query_params)

        return PySenseDashboard.Dashboard(self, resp_json)

    def add_dashboards(self, dashboards):
        """Import given dashboards.

        Args:
            dashboards: One to many PySense dashboard to import

        Returns:
            An array of new dashboards
        """
        ret_arr = []
        for dashboard in PySenseUtils.make_iterable(dashboards):
            resp = self.connector.rest_call('post', 'api/v1/dashboards', json_payload=dashboard.get_json())
            ret_arr.append(PySenseDashboard.Dashboard(self, resp))
        return ret_arr

    def delete_dashboards(self, dashboards):
        """Delete dashboards.

        Args:
            dashboards: Dashboards to delete
        """
        for dashboard in PySenseUtils.make_iterable(dashboards):
            self.connector.rest_call('delete', 'api/v1/dashboards/{}'.format(dashboard.get_id()))

    ############################################
    # Folders                                  #
    ############################################

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

    ############################################
    # Groups                                   #
    ############################################

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

    ############################################
    # Users                                    #
    ############################################

    def add_user(self, email, role, *, user_name=None, first_name=None, last_name=None,
                 groups=[], preferences={}, ui_settings={}):
        """Creates a user in Sisense.

        Args:
            email: email address for user
            role: role of user
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

    def get_users(self, *, user_name=None, email=None, first_name=None, last_name=None, role_name=None, group=None,
                  active=None, origin=None, ids=None, fields=[], sort=None, skip=None, limit=None, expand=None):
        """Returns a list of users.

        Results can be filtered by parameters such as username and email.
        The expandable fields for the user object are groups, adgroups and role.

        Args:
            user_name: (optional) Username to filter by
            email: (optional) Email to filter by
            first_name: (optional) First name to filter by
            last_name: (optional) Last name to filter by
            role_name: (optional) Role filter by
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
            'role': self.get_role_id(role_name),
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

    ############################################
    # Elasticubes                              #
    ############################################

    def get_elasticubes(self):
        """Gets elasticubes"""
        resp_json = self.connector.rest_call('get', 'api/v1/elasticubes/getElasticubes')
        ret_arr = []
        for cube in resp_json:
            ret_arr.append(PySenseElasticube.Elasticube(self, cube))
        return ret_arr

    def get_elasticube_by_name(self, name):
        """Gets elasticube with given name"""
        cubes = self.get_elasticubes()
        for cube in cubes:
            if cube.get_name() == name:
                return cube
        return None

    ############################################
    # Plug Ins                                 #
    ############################################

    def get_plugins(self, *, order_by=None, desc=None, search=None, skip=None, limit=None):
        """Get all plugins installed.

        Args:
            order_by: (optional) Filter by provided field
            desc: (optional) Order by descending/ascending (boolean)
            search: (optional) Filter according to provided string
            skip: (optional) Number of results to skip from the start of the data set.
                Skip is to be used with the limit parameter for paging.
            limit: (optional) How many results should be returned. limit is to be used with the skip parameter for paging

        Returns:
            An array of plugins
        """
        query_params = {
            'orderby': order_by,
            'desc': desc,
            'search': search,
            'skip': skip,
            'limit': limit
        }
        resp_json = self.connector.rest_call('get', 'api/v1/plugins', query_params=query_params)
        ret_arr = []
        for plugin in resp_json['plugins']:
            ret_arr.append((PySensePlugin.Plugin(self, plugin)))
        return ret_arr

    ############################################
    # Roles                                    #
    ############################################

    def get_role_id(self, role_name):
        """Get the role id for the given role name"""
        if role_name is None:
            return None
        for item in self._roles:
            if role_name == item['name'] or role_name == item['displayName']:
                return item['_id']
        raise PySenseException.PySenseException('No role with name {} found'.format(role_name))

    def get_role_name(self, role_id):
        """Get the role name for the given role id"""

        for item in self._roles:
            if role_id == item['_id']:
                return item['displayName']
        raise PySenseException.PySenseException('No role with id {} found'.format(role_id))

    ############################################
    # Connections                              #
    ############################################

    def get_connections(self, *, provider=None, sort=None, skip=None, limit=None):
        """Returns all the connections

        Args:
            provider: Type or list of types to filter for
            sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -
            skip: Number of results to skip from the start of the data set.
                Skip is to be used with the limit parameter for paging
            limit: How many results should be returned. limit is to be used with the skip parameter for paging
        """
        query_params = {
            'sort': sort,
            'skip': skip,
            'limit': limit
        }
        provider = PySenseUtils.make_iterable(provider)
        resp_json = self.connector.rest_call('get', 'api/v1/connection', query_params=query_params)
        ret_arr = []
        for connection in resp_json:
            connection = PySenseConnection.make_connection(self, connection)
            if len(provider) > 0:
                if connection.get_provider() in provider:
                    ret_arr.append(connection)
            else:
                ret_arr.append(connection)

        return ret_arr

    def get_connection_by_id(self, connection_id):
        """Returns the connection with the given id"""
        resp_json = self.connector.rest_call('get', 'api/v1/connection/{}'.format(connection_id))
        return PySenseConnection.make_connection(self, resp_json)

    def add_connection(self, connection_json):
        """Add a new connection with given connection json"""
        resp_json = self.connector.rest_call('post', 'api/v1/connection', json_payload=connection_json)
        return PySenseConnection.make_connection(self, resp_json)

    def delete_connections(self, connections):
        """Deletes the given PySense connections"""
        for connection in PySenseUtils.make_iterable(connections):
            self.connector.rest_call('delete', 'api/v1/connection/{}'.format(connection.get_id()))

    ############################################
    # Data Models                              #
    ############################################

    def add_data_model(self, data_model, *, title=None, target_data_model=None):
        """Adds a new data model to the instance.

        Sisense does not support this in Windows

        Can be used to update an existing data model by adding it to target data model.

        To add a new model with a new title
        add_data_model(model_to_add, title='New Title')

        To update an existing model
        add_data_model(new_data_model, target_data_model=old_data_model)

        If updating an existing data model, no modifications to title will happen.

        Args:
            data_model: The PySense DataModel object to import
            title: (optional) Title to give the data model
            target_data_model: (optional) The data model to update.
        """
        if self.version == SisenseVersion.Version.WINDOWS:
            raise PySenseException.PySenseException("Import data model not supported on windows")

        target_data_model_id = target_data_model.get_oid() if target_data_model is not None else None

        query_params = {'title': title, 'datamodelId': target_data_model_id}
        data_model_json = self.connector.rest_call('post', 'api/v2/datamodel-imports/schema',
                                                   query_params=query_params, json_payload=data_model.get_schema_json())

        return PySenseDataModel.DataModel(self, data_model_json)

    def get_data_models(self, *, title=None, fields=None, sort=None, limit=None, skip=None):
        """Gets data model schemas

        Sisense does not support this in Windows

        If fields is specified, PySense may experience issues.

        To get all data models:
        get_data_models()

        To get a data model called PySense:
        get_data_models(title='PySense')

        Args:
            title: (optional) Datamodel Title to search for
            fields: (optional) A whitelist of fields to return for each object in the response.
            sort: (optional) A field by which the results should be sorted.
                Results will be sorted in ascending order by default, or descending if the field name is prefixed by -.
            limit: (optional) Number of results to be returned from the data set.
                This field must be used with the skip parameter, and is intended for paging.
            skip: (optional) Number of results to skip from the start of the data set.
                This parameter must be used with the limit parameter, and is intended for paging.

        Returns:
            If title is specified, a single data model will be returned if a matching data model is found.
            Otherwise PySense will throw an exception.
            If title is not specified an array will be returned.

        """
        if self.version == SisenseVersion.Version.WINDOWS:
            raise PySenseException.PySenseException("Get data model not supported on windows")

        query_params = {
            'title': title,
            'fields': fields,
            'sort': sort,
            'limit': limit,
            'skip': skip
        }

        data_models = self.connector.rest_call('get', 'api/v2/datamodels/schema', query_params=query_params)
        if title is not None:
            if data_models is not None:
                return PySenseDataModel.DataModel(self, data_models)
            else:
                raise PySenseException.PySenseException('No data model with name {} found'.format(title))
        else:
            ret_arr = []
            for data_model in data_models:
                ret_arr.append(PySenseDataModel.DataModel(self, data_model))
            return ret_arr

    def delete_data_model(self, data_models):
        """Deletes the given data models

        Args:
            data_models: One to many data models to delete
        """
        if self.version == SisenseVersion.Version.WINDOWS:
            raise PySenseException.PySenseException("Delete data model not supported on windows")

        for data_model in PySenseUtils.make_iterable(data_models):
            self.connector.rest_call('delete', 'api/v2/datamodels/{}'.format(data_model.get_oid()))



