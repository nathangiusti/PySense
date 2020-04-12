import yaml

from PySense import PySenseDashboard
from PySense import PySenseElasticube
from PySense import PySenseException
from PySense import PySenseGroup
from PySense import PySenseFolder
from PySense import PySensePlugin
from PySense import PySenseRestConnector
from PySense import PySenseUser
from PySense import PySenseUtils


def authenticate_by_file(config_file):
    """
    Creates a new PySense client with the credentials in the given config file.  

    :param config_file: Yaml file with entries for host, username, and password  
    
    :return: A new PySense client for the given credentials  
    """
    
    with open(config_file, 'r') as yml_file:
        cfg = yaml.safe_load(yml_file)
        debug = cfg['debug'] if 'debug' in cfg else False
        return PySense(cfg['host'], cfg['username'], cfg['password'], debug=debug)


class PySense:

    def __init__(self, host, username, password, *, debug=False):
        self.connector = PySenseRestConnector.RestConnector(host, username, password, debug)
        
    def set_debug(self, debug):
        """
        Enable or disable logging of REST api calls to std out. Use for debugging. Debug is false by default.    
          
        :param debug:  True or False to enable or disable debug. 
        """
        self.connector.debug = debug

    ############################################
    # Dashboards                               #
    ############################################

    def get_dashboards(self, *, parent_folder_name=None, name=None, data_source_title=None,
                       data_source_address=None, fields=None, sort=None, expand=None):
        """
        Get all dashboards   
          
        Optional:  
        :param parent_folder_name: Parent folder name to filter by  
        :param name: Name to filter by  
        :param data_source_title: Data source name to filter by  
        :param data_source_address: Data source address to filter by  
        :param fields: Whitelist of fields to return for each document.  
           Can also exclude by prefixing field names with -  
        :param sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -  
        :param expand: List of fields that should be expanded  
          
        :return: All found dashboards  
        """
        
        ret_arr = []
        folder_id = None
        if parent_folder_name:
            folders = self.get_folders(name=parent_folder_name)
            if len(folders) == 1:
                folder_id = folders[0].get_id()
            else:
                raise Exception("{} folders found with name {}".format(len(folders), parent_folder_name))

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
        for dash in json_arr:
            ret_arr.append(PySenseDashboard.Dashboard(self.connector, dash))
        return ret_arr

    def get_dashboard_by_id(self, dashboard_id, *, fields=None, expand=None):
        """  
        Returns a specific dashboard object by ID.  
  
        :param dashboard_id: The ID of the dashboard to get  
          
        Optional:  
        :param fields: Whitelist of fields to return for each document. fields Can also define which fields to exclude
            by prefixing field names with -  
        :param expand: List of fields that should be expanded (substitures their IDs with actual objects). May be nested
            using the resource.subResource format  
              
        :return: Dashboard with id given  
        """
        
        query_params = {
            'fields': fields,
            'expand': expand
        }
        
        resp_json = self.connector.rest_call('get', 'api/v1/dashboards/{}'.format(dashboard_id),
                                             query_params=query_params)
        
        return PySenseDashboard.Dashboard(self.connector, resp_json)

    def post_dashboards(self, dashboard_json):
        """  
        Import given dashboard  

        :param dashboard_json: The dashboard json from the dash file  
        
        :return: The dashboard given by the response object  
        """
        
        resp = self.connector.rest_call('post', 'api/v1/dashboards', json_payload=dashboard_json)
        return PySenseDashboard.Dashboard(self.connector, resp)

    def delete_dashboards(self, dashboard_id):
        """  
        Delete dashboard with id  

        :param dashboard_id: The ID of the dashboard to delete  
        
        :return: The response object  
        """
        self.connector.rest_call('delete', 'api/v1/dashboards/{}'.format(dashboard_id))

    ############################################
    # Folders                                  #
    ############################################

    def get_folders(self, *, name=None, structure=None, ids=None, fields=None,
                    sort=None, skip=None, limit=None, expand=None):
        """  
        Provides access to a specified user’s folders in their stored format  
  
        Optional: 
        :param name: Name to filter by  
        :param structure: Structure type of the folders  
        :param ids: Array of folder IDs to get, separated by a comma (,) and without spaces  
        :param fields: Whitelist of fields to return for each document. fields Can also define which fields to exclude  
            by prefixing field names with -  
        :param sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -  
        :param skip: Number of results to skip from the start of the data set. skip is to be used with the limit  
            parameter for paging  
        :param limit: How many results should be returned. limit is to be used with the skip parameter for paging  
        :param expand: List of fields that should be expanded (substitue their IDs with actual objects). May be  
            nested using the resource.subResource format  
            
        :return: An array of folders matching the search criteria  
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
                    ret_arr.append(PySenseFolder.Folder(self.connector, folder))
        else:
            for folder in resp_json:
                ret_arr.append(PySenseFolder.Folder(self.connector, folder))
        return ret_arr

    ############################################
    # Groups                                   #
    ############################################

    def get_groups(self, *, name=None, mail=None, role=None, origin=None, ids=None, fields=None,
                   sort=None, skip=None, limit=None, expand=None):
        """  
        Returns a list of user groups with their details.  
        The results can be filtered by different parameters such as group name or origin.  

        Optional: 
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
        """
        
        query_params = {
            'name': name,
            'mail': mail,
            'roleId': self.connector.get_role_id(role),
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
            ret_arr.append(PySenseGroup.Group(self.connector, group))
        return ret_arr

    def get_groups_by_name(self, groups):
        """  
        :param groups: A name or list of names 
          
        :return: An array of groups for that name
        """
        
        if groups is None:
            return []
        
        resp_json = self.connector.rest_call('get', 'api/v1/groups')
        ret = []
        for group in PySenseUtils.make_iterable(groups):
            found = False
            for item in resp_json:
                if group == item['name']:
                    ret.append(PySenseGroup.Group(self.connector, item))
                    found = True
            if not found:
                raise PySenseException.PySenseException('Cannot find group with name {}'.format(group))
        return ret

    def add_groups(self, names):
        """  
        Add groups with given names  

        :param names: One to many names 
          
        :return: Array of new groups  
        """
        ret_arr = []
        for name in PySenseUtils.make_iterable(names):
            payload = {'name': name}
            resp_json = self.connector.rest_call('post', 'api/v1/groups', json_payload=payload)
            ret_arr.append(PySenseGroup.Group(self.connector, resp_json))
        return ret_arr

    def delete_groups(self, groups):
        """  
        Delete groups with given names  

        :param groups: Groups to delete
        """
        for group in PySenseUtils.make_iterable(groups):
            self.connector.rest_call('delete', 'api/groups/{}'.format(group.get_id()))

    ############################################
    # Users                                    #
    ############################################

    def add_user(self, email, role, *, user_name=None, first_name=None, last_name=None,
                 groups=[], preferences={}, ui_settings={}):
        """  
        Creates that user in SiSense, returning the created object.  

        :param email: email address for user  
        :param role: role of user  
        
        Optional:  
        :param user_name: User user name. Email used if None  
        :param first_name: User first name   
        :param last_name: User last name  
        :param groups: The groups to add the user to  
        :param preferences: User preferences  
        :param ui_settings: User ui settings  
          
        :return: Newly created user object  
        """  
        
        user_obj = {
            'email': email,
            'username': user_name if user_name is not None else email,
            'roleId': self.connector.get_role_id(role)
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
        return PySenseUser.User(self.connector, resp_json)

    def get_users(self, *, user_name=None, email=None, first_name=None, last_name=None, role_name=None, group=None,
                  active=None, origin=None, ids=None, fields=None, sort=None, skip=None, limit=None, expand=None):
        """  
        Returns a list of users with their details.  
        Results can be filtered by parameters such as username and email.  
        The expandable fields for the user object are groups, adgroups and role.  

        Optional:
        :param user_name: Username to filter by  
        :param email: Email to filter by  
        :param first_name: First name to filter by  
        :param last_name: Last name to filter by  
        :param role_name: Role filter by  
        :param group: Group to filter by  
        :param active: User state to filter by (true for active users, false for inactive users)  
        :param origin: User origin to filter by (ad for active directory or sisense)  
        :param ids: Array of user ids to get separated by comma and without spaces  
        :param fields: Whitelist of fields to return for each document.  
            Fields can also define which fields to exclude by prefixing field names with -  
        :param sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -  
        :param skip: Number of results to skip from the start of the data set.  
            Skip is to be used with the limit parameter for paging  
        :param limit: How many results should be returned. limit is to be used with the skip parameter for paging  
        :param expand: List of fields that should be expanded (substitutes their IDs with actual objects).  
            May be nested using the resource.subResource format  

        :return: An array of users objects  
        """
        
        query_params = {
            'userName': user_name,
            'email': email,
            'firstName': first_name,
            'lastName': last_name,
            'role': self.connector.get_role_id(role_name),
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
            ret_arr.append((PySenseUser.User(self.connector, user)))
        return ret_arr

    def delete_users(self, users):
        """  
        Deletes the specified user or users  
  
        :param users: User obj to delete  
           
        """
        for user in PySenseUtils.make_iterable(users):
            self.connector.rest_call('delete', 'api/v1/users/{}'.format(user.get_id()))

    ############################################
    # Elasticubes                              #
    ############################################

    def get_elasticubes(self):
        """  
        Gets elasticubes  
  
        :return: An array of elasticubes   
        """
        resp_json = self.connector.rest_call('get', 'api/v1/elasticubes/getElasticubes')
        ret_arr = []
        for cube in resp_json:
            ret_arr.append(PySenseElasticube.Elasticube(self.connector, cube))
        return ret_arr

    def get_elasticube_by_name(self, name):
        """  
        Gets elasticube by name  

        :param name: Name of elasticube to get  
        
        :return: A single elasticube with the given name or None if not found  
        """
        
        cubes = self.get_elasticubes()  
        for cube in cubes:  
            if cube.get_name() == name:
                return cube
        return None

    ############################################
    # Plug Ins                                 #
    ############################################
    
    def get_plugins(self, *, order_by=None, desc=None, search=None, skip=None, limit=None):
        """
        Get all plugins installed  
          
        Optional:  
        :param order_by: Filter by provided field  
        :param desc: Order by descending/ascending (boolean)  
        :param search: Filter according to provided string  
        :param skip: Number of results to skip from the start of the data set. 
            Skip is to be used with the limit parameter for paging.  
        :param limit: How many results should be returned. limit is to be used with the skip parameter for paging
          
        :return: An array of PySense Plugins Objects
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
            ret_arr.append((PySensePlugin.Plugin(self.connector, plugin)))
        return ret_arr
