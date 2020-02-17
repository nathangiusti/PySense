import json
import requests
import yaml
import re

import PySenseAlert
import PySenseDashboard
import PySenseUtils


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
         :param fields: Whitelist of fields to return for each document. Can also exclude by prefixing field names with -
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
                    folder_id = folders[0]['oid']
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
        param_string = PySenseUtils.build_query_string({
            'fields': fields,
            'expand': expand
        })
        resp = requests.get('{}/api/v1/dashboards/{}?{}'.format(self.host, dashboard_id, param_string),
                            headers=self.token)
        return PySenseUtils.response_successful(resp,
                                                success=PySenseDashboard.Dashboard(self.host, self.token, resp.json()))

    def post_dashboards_import_bulk(self, dashboard_file, param_string):
        resp = requests.post('{}/api/v1/dashboards/import/bulk?{}'.format(self.host, param_string),
                             headers=self.token, json=json.loads(dashboard_file))
        return PySenseUtils.response_successful(resp)

    def post_dashboards(self, dashboard_obj):
        """
        Import given dashboard

        :param dashboard_obj: The JSON dashboard object
        :return: The response object or None on failure
        """
        resp = requests.post('{}/api/v1/dashboards/'.format(self.host, dashboard_obj), headers=self.token,
                             json=json.loads(dashboard_obj))
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

    def post_dashboards_import_bulk(self, dashboard, param_dict):
        param_string = PySenseUtils.build_query_string(param_dict)
        return PySenseDashboard.post_dashboards_import_bulk(dashboard, param_string)

    def post_dashboards_import_bulk(self, dashboard, action=None, republish=None, importFolder=None):
        param_string = PySenseUtils.build_query_string({
            'action': action,
            'republish': republish,
            'importFolder': importFolder
        })
        return PySenseDashboard.post_dashboards_import_bulk(dashboard, param_string)

    ############################################
    # Folders                                  #
    ############################################

    def get_folders(self, name=None, structure=None, ids=None, fields=None,
                    sort=None, skip=None, limit=None, expand=None):
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
                        ret_arr.append(folder)
                return ret_arr
            else:
                return resp.json()
        return None

    def get_folders_id(self, folder_id):
        resp = requests.get('{}/api/v1/folders/{}'.format(self.host, folder_id), headers=self.token)
        return PySenseUtils.response_successful(resp, success=resp.json())

    ############################################
    # Widgets                                  #
    ############################################

    def move_widget(self, source_dashboard_id, destination_dashboard_id, widget_id):
        if self.copy_widget(source_dashboard_id, destination_dashboard_id, widget_id):
            resp = self.delete_dashboards_widgets(source_dashboard_id, widget_id)
            return PySenseUtils.response_successful(resp)
        else:
            return None

    def copy_widget(self, source_dashboard_id, destination_dashboard_id, widget_id):
        widget = self.get_dashboards_widget(source_dashboard_id, widget_id)
        if widget:
            resp = self.post_dashboards_widgets(destination_dashboard_id, widget)
            return PySenseUtils.response_successful(resp)
        else:
            return None

    ############################################
    # Groups                                   #
    ############################################

    def get_group_ids(self, groups):
        resp = requests.get('{}/api/v1/groups'.format(self.host),
                            headers=self.token)
        if PySenseUtils.response_successful(resp):
            json_rep = json.loads(resp.content.decode('utf8'))
            ret = []
            for group in groups:
                found = False
                for item in json_rep:
                    if group == item['_id'] or group == item['name']:
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


    def post_user(self, email, username, roleId, firstName=None, lastName=None, groups=[], preferences={}, uiSettings={}):
        role_id = self.get_role_id(roleId)
        if not role_id:
            return "Role {} not found".format(roleId)
        groups_obj = self.get_group_ids(groups)
        user_obj = {
            'email': email,
            'username': username,
            'firstName': firstName,
            'lastName': lastName,
            'roleId': role_id,
            'groups': groups_obj,
            'preferences': preferences,
            'uiSettings': uiSettings
        }
        return self.post_user_obj(user_obj)


    def post_user_obj(self, user_obj):
        resp = requests.post('{}/api/v1/users'.format(self.host), headers=self.token,
                             json=user_obj)
        PySenseUtils.response_successful(resp)


    def delete_user(self, user):
        if user.find('@') > 0:
            user_id = PySenseUtils.get_user_id_by_email(user)
        else:
            user_id = user
        resp = requests.delete('{}/api/v1/users/{}'.format(PySenseConfig.host, user_id), headers=PySenseConfig.token)
        PySenseUtils.response_successful(resp)

    def get_role_id(self, role_id):
        resp = requests.get('{}/api/roles'.format(self.host),
                            headers=self.token)
        if not PySenseUtils.response_successful(resp):
            return

        json_rep = json.loads(resp.content.decode('utf8'))
        for item in json_rep:
            if role_id == item['_id'] or role_id == item['name'] or role_id == item['displayName']:
                return item['_id']

    def get_user_id(self, userName=None, email=None):
        param_string = PySenseUtils.build_query_string({
            'userName': userName,
            'email': email
        })
        resp = requests.get('{}/api/v1/users?{}'.format(self.host, param_string),
                            headers=self.token)
        if not PySenseUtils.response_successful(resp):
            return None
        json_rep = json.loads(resp.content.decode('utf8'))
        if len(json_rep) == 1:
            return json_rep[0]['_id']
        else:
            print('{} users found with {}'.format(len(json_rep), param_string))
            return None

    ############################################
    # Alerts                                   #
    ############################################

    def post_alert(self, alert_obj):
        resp = requests.post('{}/api/v1/alerts'.format(self.host),
                             headers=self.token, json=json.loads(alert_obj))
        PySenseUtils.response_successful(resp)

    def post_alert(self, user, name):
        alert_obj = PySenseAlert.createAlert(user, name)
        return post_alert(alert_obj)

