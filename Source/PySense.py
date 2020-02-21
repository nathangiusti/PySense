import json
import requests
import yaml
import re

import PySenseAlert
import PySenseDashboard
import PySenseUtils
import PySenseFolder
import PySenseUser


def authenticate_by_file(config_file):
    with open(config_file, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        return PySense(cfg['host'], cfg['username'], cfg['password'])


class PySense:
    token = None
    host = None

    def __init__(self, host, username, password):
        """
        Authenticates with Sisense. Saves host and user token.

        :param host: the host address
        :param username: Username
        :param password: Password
        :return: True if successful, else false
        """

        data = {'username': username, 'password': password}
        host = PySenseUtils.format_host(host)
        resp = requests.post('{}/api/v1/authentication/login'.format(host), data=data)
        if PySenseUtils.response_successful(resp):
            access_code = "Bearer " + resp.json()['access_token']
            self.token = {'authorization': access_code}
            self.host = host

    def get_authentication(self):
        """
        Returns authentication parameters
        @return: A dictionary with an entry for host and token
        """
        if self.host and self.token:
            return {'host': self.host, 'token': self.token}
        else:
            return None

    ############################################
    # Dashboards                               #
    ############################################

    def get_dashboards(self, parentFolder=None, name=None, datasourceTitle=None,
                       datasourceAddress=None, fields=None, sort=None, expand=None):
        """
         Get all dashboards

         :param parentFolder: Parent folder ID or name to filter by
         :param name: Name to filter by
         :param datasourceTitle: Data source name to filter by
         :param datasourceAddress: Data source address to filter by
         :param fields: Whitelist of fields to return for each document.
            Can also exclude by prefixing field names with -
         :param sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -
         :param expand: List of fields that should be expanded
         :return: All found dashboards
         """
        ret_arr = []
        folder_id = None
        if parentFolder:
            if re.match(r"^[0-9a-fA-F]{24}$", parentFolder):
                folder_id = parentFolder
            else:
                folders = self.get_folders(name=parentFolder)
                if len(folders) == 1:
                    folder_id = folders[0].get_folder_oid()
                else:
                    print("{} folders found with name {}".format(len(folders), parentFolder))
                    return None

        param_string = PySenseUtils.build_query_string({
            'parentFolder': folder_id,
            'name': name,
            'datasourceTitle': datasourceTitle,
            'datasourceAddress': datasourceAddress,
            'fields': fields,
            'sort': sort,
            'expand': expand
        })
        resp = requests.get('{}/api/v1/dashboards?{}'.format(self.host, param_string),
                            headers=self.token)

        if PySenseUtils.response_successful(resp):
            json_arr = json.loads(resp.content)
            for dash in json_arr:
                ret_arr.append(PySenseDashboard.Dashboard(self.host, self.token, dash))
            return ret_arr
        else:
            return None

    def get_dashboards_id(self, dashboard_id, fields=None, expand=None):
        """
        Returns a specific dashboard object by ID.

        :param dashboard_id: The ID of the dashboard to get
        :param fields: Whitelist of fields to return for each document. fields Can also define which fields to exclude
            by prefixing field names with -
        :param expand: List of fields that should be expanded (substitures their IDs with actual objects). May be nested
            using the resource.subResource format
        :return: Dashboard with id given or None on error
        """
        param_string = PySenseUtils.build_query_string({
            'fields': fields,
            'expand': expand
        })
        resp = requests.get('{}/api/v1/dashboards/{}?{}'.format(self.host, dashboard_id, param_string),
                            headers=self.token)
        return PySenseUtils.response_successful(resp,
                                                success=PySenseDashboard.Dashboard(self.host, self.token, resp.json()))

    def post_dashboards(self, dashboard_obj):
        """
        Import given dashboard

        :param dashboard_obj: A PySense dashboard object
        :return: The dashboard given by the response object or None on failure
        """
        resp = requests.post('{}/api/v1/dashboards/'.format(self.host), headers=self.token,
                             json=dashboard_obj.get_dashboard_json())
        return PySenseUtils.response_successful(resp,
                                                success=PySenseDashboard.Dashboard(
                                                    self.host, self.token, json.loads(resp.content)))

    def delete_dashboards(self, dashboard_id):
        """
        Delete dashboard with id

        :param dashboard_id: The ID of the dashboard to delete
        :return: The response object or None on failure
        """
        resp = requests.delete('{}/api/v1/dashboards/{}'.format(self.host, dashboard_id),
                               headers=self.token)
        return PySenseUtils.response_successful(resp)

    ############################################
    # Folders                                  #
    ############################################

    def get_folders(self, name=None, structure=None, ids=None, fields=None,
                    sort=None, skip=None, limit=None, expand=None):
        """
        Prrovides access to a specified user’s folders in their stored format

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
        @return:
        """
        ret_arr = []
        param_string = PySenseUtils.build_query_string({
            'name': name,
            'structure': structure,
            'ids': ids,
            'fields': fields,
            'sort': sort,
            'skip': skip,
            'limit': limit,
            'expand': expand
        })
        resp = requests.get('{}/api/v1/folders?{}'.format(self.host, param_string),
                            headers=self.token)
        if PySenseUtils.response_successful(resp):
            # Sisense Rest API always returns the root folder, so we filter it out when looking by name
            if name:
                for folder in resp.json():
                    if folder['name'] == name:
                        ret_arr.append(PySenseFolder.Folder(self.host, self.token, folder))
            else:
                for folder in resp.json():
                    ret_arr.append(PySenseFolder.Folder(self.host, self.token, folder))
            return ret_arr
        return None

    def get_folders_id(self, folder_id):
        """
        Get a specific folder by folder id

        @param folder_id: The folder id of the folder
        @return: A PySense folder object of the folder or None on error
        """
        resp = requests.get('{}/api/v1/folders/{}'.format(self.host, folder_id), headers=self.token)
        return PySenseUtils.response_successful(resp, success=PySenseFolder.Folder(self.host, self.token, resp.json()))

    ############################################
    # Groups                                   #
    ############################################

    def get_group_ids(self, groups):
        """
        Get the ids for groups
        @param groups: An array of group names
        @return: An array of ids for the groups, None on rest error
        """
        resp = requests.get('{}/api/v1/groups'.format(self.host),
                            headers=self.token)
        if PySenseUtils.response_successful(resp):
            json_rep = json.loads(resp.content.decode('utf8'))
            ret = []
            for group in groups:
                found = False
                for item in json_rep:
                    if group == item['name']:
                        ret.append(item['_id'])
                        found = True
                if not found:
                    return 'Cannot find id for group {}'.format(group)
            return ret
        else:
            return None

    ############################################
    # Users                                    #
    ############################################

    def post_user(self, email, username, role, firstName=None, lastName=None,
                  groups=None, preferences=None, uiSettings=None):
        """
        Receives a new user object and creates that user in Sisense, returning the created object.
        If a user with the same username or email exists, it will return an error.

        @param email: email address for user
        @param username: username
        @param role: role name
        @param firstName: user first name
        @param lastName: user last name
        @param groups: The groups to add the user to
        @param preferences: User preferences
        @param uiSettings: User ui settings
        @return: Newly created user object or None on error
        """
        role_id = PySenseUtils.get_role_id(self.host, self.token, role)
        if not role_id:
            return "Role {} not found".format(role)
        groups_obj = self.get_group_ids(groups)
        user_obj = PySenseUtils.build_json_object({
            'email': email,
            'username': username,
            'firstName': firstName,
            'lastName': lastName,
            'roleId': role_id,
            'groups': groups_obj,
            'preferences': preferences,
            'uiSettings': uiSettings
        })
        resp = requests.post('{}/api/v1/users'.format(self.host), headers=self.token,
                             json=user_obj)
        return PySenseUtils.response_successful(resp, success=PySenseUser.User(
            self.host, self.token, json.loads(resp.content)))

    def get_users(self, userName=None, email=None, firstName=None, lastName=None, role=None, group=None, active=None,
                  origin=None, ids=None, fields=None, sort=None, skip=None, limit=None, expand=None):
        """
        Returns a list of users with their details.
        Results can be filtered by parameters such as username and email.
        The expandable fields for the user object are groups, adgroups and role.

        @param userName: Username to filter by
        @param email: Email to filter by
        @param firstName: First name to filter by
        @param lastName: Last name to filter by
        @param role: Role filter by
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

        @return: An array of users objects or None on error
        """
        role_id = PySenseUtils.get_role_id(self.host, self.token, role)
        if not role_id:
            return "Role {} not found".format(role)

        param_string = PySenseUtils.build_query_string({
            'userName': userName,
            'email': email,
            'firstName': firstName,
            'lastName': lastName,
            'role': role_id,
            'group': group,
            'active': active,
            'origin': origin,
            'ids': ids,
            'fields': fields,
            'sort': sort,
            'skip': skip,
            'limit': limit,
            'expand': expand
        })
        resp = requests.get('{}/api/v1/users?{}'.format(self.host, param_string), headers=self.token)
        ret_arr = []
        if PySenseUtils.response_successful(resp):
            for user in json.loads(resp):
                ret_arr.append((PySenseUser.User(self.host, self.token, user)))
            return ret_arr
        else:
            None

    def delete_user(self, user):
        """
        Deletes the specified user
        @param user: User obj to delete
        @return: Response or None on error
        """
        resp = requests.delete('{}/api/v1/users/{}'.format(self.host, user.get_user_id()), headers=self.token)
        return PySenseUtils.response_successful(resp)

    ############################################
    # Alerts                                   #
    ############################################
    # This isn't at all done
    def post_alert(self, alert_obj):
        resp = requests.post('{}/api/v1/alerts'.format(self.host),
                             headers=self.token, json=json.loads(alert_obj))
        PySenseUtils.response_successful(resp)


