import json
import requests
import yaml
import re

import PySenseConfig
import PySenseDashboard
import PySenseFolder
import PySenseUtils

############################################
# Authentication and configuration methods #
############################################


def set_host(host):
    """
    Set host manually. Host is automatically set when calling authenticate
    @param host: The new host
    @return: The host as it is set
    """
    PySenseConfig.host = PySenseUtils.format_host(host)
    return PySenseConfig.host


def get_host():
    """

    @return: Returns the current host string
    """
    return PySenseConfig.host


def check_authentication():
    """
    Returns authentication parameters
    @return: A dictionary with an entry for host and token
    """
    return {'host': PySenseConfig.host, 'token': PySenseConfig.token}


def authenticate(host, username, password):
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
        PySenseConfig.token = {'authorization': access_code}
        PySenseConfig.host = host
        return True
    return False


def authenticate_by_file(config_file):
    """
    Authenticates with Sisense via settings in file. Saves host and user token.

    :param config_file: The yaml file with authentication settings
    :return: True if successful, else false
    """
    with open(config_file, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        return authenticate(cfg['host'], cfg['username'], cfg['password'])

############################################
# Dashboards                               #
############################################


def get_dashboards(param_dict):
    """
    Get all dashboards

    :param param_dict: Dictionary of search parameters
    :return: All found dashboards
    """
    return PySenseDashboard.get_dashboards(PySenseUtils.build_query_string(param_dict))


def get_dashboards(parentFolder=None, name=None, datasourceTitle=None,
                   datasourceAddress=None, fields=None, sort=None, expand=None):
    """
     Get all dashboards

     :param parentfolder: Parent folder ID or name to filter by
     :param name: Name to filter by
     :param datasourceTitle: Data source name to filter by
     :param datasourceAddress: Data source address to filter by
     :param fields: Whitelist of fields to return for each document. Can also exclude by prefixing field names with -
     :param sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -
     :param expand: List of fields that should be expanded
     :return: All found dashboards
     """
    if re.match(r"^[0-9a-fA-F]{24}$", parentFolder):
        folder_id = parentFolder
    else:
        folder_id = get_folder_by_name(parentFolder)

    if not folder_id:
        print("Folder {} not found".format(parentFolder))

    param_string = PySenseUtils.build_query_string({
        'parentFolder': folder_id,
        'name': name,
        'datasourceTitle': datasourceTitle,
        'datasourceAddress': datasourceAddress,
        'fields': fields,
        'sort': sort,
        'expand': expand
    })
    return PySenseDashboard.get_dashboards(param_string)


def get_dashboard_export_png(dashboard_id, path, param_dict):
    """
     Get dashboard as png

     :param dashboard_id: The ID of the dashboard to export
     :param path: Path to save location of png
     :param param_dict: Dictionary of parameters
     :return: The path of the created file or None on error
     """
    param_string = PySenseUtils.build_query_string(param_dict)
    return PySenseDashboard.get_dashboard_export_png(dashboard_id, path, param_string)


def get_dashboard_export_png(dashboard_id, path, includeTitle=None, includeFilters=None, includeDs=None, width=None):
    """
     Get dashboard as png

     :param dashboard_id: The ID of the dashboard to export
     :param path: Path to save location of png
     :param includeTitle: Should dashboard title be included in the exported file
     :param includeFilters: Should dashboard filters be included in the exported file
     :param includeDs: Should dashboard datasource info be included in the exported file
     :param width: Render width in pixels
     :return: The path of the created file or None on error
     """
    param_string = PySenseUtils.build_query_string({
        'includeTitle': includeTitle,
        'includeFilters': includeFilters,
        'includeDs': includeDs,
        'width': width
    })
    return PySenseDashboard.get_dashboard_export_png(dashboard_id, path, param_string)


def get_dashboard_export_pdf(dashboard_id, path, param_dict):
    """
     Get dashboard as pdf

     :param dashboard_id: The ID of the dashboard to export
     :param path: Path to save location of pdf
     :param param_dict: Dictionary of parameters
     :return: The path of the created file or None on error
     """
    # Paper format, paper orientation, and layout are required
    if 'paperFormat' in param_dict and 'paperOrientation' in param_dict and 'layout' in param_dict:
        param_string = PySenseUtils.build_query_string(param_dict)
        return PySenseDashboard.get_dashboard_export_pdf(dashboard_id, path, param_string)
    else:
        return None


def get_dashboard_export_pdf(dashboard_id, path, paperFormat, paperOrientation, layout,
                             includeTitle=None, includeFilters=None, includeDs=None, widgetid=None, preview=None,
                             rowCount=None, showTitle=None, showFooter=None, title=None, titleSize=None,
                             titlePosition=None):
    """
    Get dashboard as pdf

    :param dashboard_id: The ID of the dashboard to export
    :param path: Path to save location of pdf
    :param paperFormat: What paper format should be used while rendering the dashboard
    :param paperOrientation: What paper orientation should be used while rendering the dashboard
    :param layout: What layout should be used while rendering the dashboard, as is or feed
    :param includeTitle: Should dashboard title be included in the exported file
    :param includeFilters: Should dashboard filters be included in the exported file
    :param includeDs: Should dashboard datasource info be included in the exported file
    :param widgetid: Widget Id (Use only for Table and Pivot Widgets)
    :param preview: Should use a new Pixel Perfect Reporting
    :param rowCount: Count of Table/Pivot rows to export
    :param showTitle: Should Table/Pivot Widget title be included in the exported file
    :param showFooter: Should Table/Pivot Widget footer be included in the exported file
    :param title: Table/Pivot Widget title text in the exported file
    :param titleSize: Table/Pivot widget title size in the exported file
    :param titlePosition: Table/Pivot widget title position in the exported file
    :return: The path of the created file or None on error
    """
    param_string = PySenseUtils.build_query_string({
        'paperFormat': paperFormat,
        'paperOrientation': paperOrientation,
        'layout': layout,
        'includeTitle': includeTitle,
        'includeFilters': includeFilters,
        'includeDs': includeDs,
        'widgetid': widgetid,
        'preview': preview,
        'rowCount': rowCount,
        'showTitle': showTitle,
        'showFooter': showFooter,
        'title': title,
        'titleSize': titleSize,
        'titlePosition': titlePosition
    })
    return PySenseDashboard.get_dashboard_export_pdf(dashboard_id, path, param_string)


def post_dashboards_import_bulk(dashboard_id, param_dict):
    param_string = PySenseUtils.build_query_string(param_dict)
    return PySenseDashboard.post_dashboards_import_bulk(dashboard_id, param_string)


def post_dashboards_import_bulk(dashboard_id, action=None, republish=None, importFolder=None):
    param_string = PySenseUtils.build_query_string({
        'action': action,
        'republish': republish,
        'importFolder': importFolder
    })
    return PySenseDashboard.post_dashboards_import_bulk(dashboard_id, param_string)


def post_dashboard_widget_export_png(dashboard_id, widget_id, path, param_dict):
    if 'width' in param_dict and 'height' in param_dict:
        param_string = PySenseUtils.build_query_string(param_dict)
        return PySenseDashboard.post_dashboard_widget_export_png(dashboard_id, widget_id, path, param_string)
    else:
        return None


def post_dashboard_widget_export_png(dashboard_id, widget_id, path, width, height):
    param_string = PySenseUtils.build_query_string({
        'width': width,
        'height': height
    })
    return PySenseDashboard.post_dashboard_widget_export_png(dashboard_id, widget_id, path, param_string)


def get_dashboard_export_dash(dashboard_id, path):
    resp = requests.get('{}/api/v1/dashboards/{}/export/dash'.format(PySenseConfig.host, dashboard_id), headers=PySenseConfig.token)
    if PySenseUtils.response_successful(resp):
        with open(path, 'wb') as out_file:
            out_file.write(resp.content)
        return path
    else:
        return None

############################################
# Folders                                  #
############################################


def get_folders(param_dict):
    return PySenseFolder.get_folders(PySenseUtils.build_query_string(param_dict))


def get_folders(name=None, structure=None, ids=None, fields=None,
                sort=None, skip=None, limit=None, expand=None):
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
    return PySenseFolder.get_folders(param_string)

def get_folder_by_name(folder_name):
    folders = get_folders(name=folder_name)
    for folder in folders:
        if folder['name'] == folder_name:
            return folder
    return None


############################################
# Widgets                                  #
############################################


def get_dashboards_widget(dashboard_id, widget_id):
    resp = requests.get('{}/api/v1/dashboards/{}/widgets/{}'.format(PySenseConfig.host, dashboard_id, widget_id),
                        headers=PySenseConfig.token)
    if PySenseUtils.response_successful(resp):
        return resp.content
    else:
        return None


def get_dashboards_widgets(dashboard_id):
    resp = requests.get('{}/api/v1/dashboards/{}/widgets'.format(PySenseConfig.host, dashboard_id),
                        headers=PySenseConfig.token)
    if PySenseUtils.response_successful(resp):
        return resp.content
    else:
        return None


def post_dashboards_widgets(dashboard_id, widget):
    widget_str = widget.decode("utf-8")
    resp = requests.post('{}/api/v1/dashboards/{}/widgets'.format(PySenseConfig.host, dashboard_id),
                         headers=PySenseConfig.token, json=json.loads(widget_str))
    if PySenseUtils.response_successful(resp):
        return resp
    else:
        return None


def delete_dashboards_widgets(dashboard_id, widget_id):
    resp = requests.delete('{}/api/v1/dashboards/{}/widgets/{}'.format(PySenseConfig.host, dashboard_id, widget_id),
                           headers=PySenseConfig.token)
    if PySenseUtils.response_successful(resp):
        return resp


def move_widget(source_dashboard_id, destination_dashboard_id, widget_id):
    if copy_widget(source_dashboard_id, destination_dashboard_id, widget_id):
        resp = delete_dashboards_widgets(source_dashboard_id, widget_id)
        if PySenseUtils.response_successful(resp):
            return resp
        else:
            return None


def copy_widget(source_dashboard_id, destination_dashboard_id, widget_id):
    widget = get_dashboards_widget(source_dashboard_id, widget_id)
    if widget:
        resp = post_dashboards_widgets(destination_dashboard_id, widget)
        if PySenseUtils.response_successful(resp):
            return resp
        else:
            return None


############################################
# Groups                                   #
############################################


def get_group_ids(groups):
    resp = requests.get('{}/api/v1/groups'.format(PySenseConfig.host),
                        headers=PySenseConfig.token)
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

############################################
# Users                                    #
############################################


def post_user(email, username, roleId, firstName=None, lastName=None, groups=[], preferences={}, uiSettings={}):
    role_id = get_role_id(roleId)
    if not role_id:
        return "Role {} not found".format(roleId)
    groups_obj = get_group_ids(groups)
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
    return post_user_obj(user_obj)


def post_user_obj(user_obj):
    resp = requests.post('{}/api/v1/users'.format(PySenseConfig.host), headers=PySenseConfig.token,
                         json=user_obj)
    if PySenseUtils.response_successful(resp):
        return resp
    else:
        None

def delete_user(user):
    if user.find('@') > 0:
        user_id = PySenseUtils.get_user_id_by_email(user)
    else:
        user_id = user
    resp = requests.delete('{}/api/v1/users/{}'.format(PySenseConfig.host, user_id), headers=PySenseConfig.token)
    if PySenseUtils.response_successful(resp):
        return resp
    else:
        None


def get_role_id(role_id):
    resp = requests.get('{}/api/roles'.format(PySenseConfig.host),
                        headers=PySenseConfig.token)
    json_rep = json.loads(resp.content.decode('utf8'))
    for item in json_rep:
        if role_id == item['_id'] or role_id == item['name'] or role_id == item['displayName']:
            return item['_id']
    return None


def get_user_id_by_email(email):
    resp = requests.get('{}/api/v1/users?email={}'.format(PySenseConfig.host, email),
                        headers=PySenseConfig.token)
    json_rep = json.loads(resp.content.decode('utf8'))
    if len(json_rep) == 1:
        return json_rep[0]['_id']
    else:
        print('{} users found with email address {}'.format(len(json_rep), email))
        return None
