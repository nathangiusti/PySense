import json
import requests

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

############################################
# Dashboards                               #
############################################


def get_dashboards(param_dict):
    return PySenseDashboard.get_dashboards(PySenseUtils.build_query_string(param_dict))


def get_dashboards(parentFolder_id=None, name=None, datasourceTitle=None,
                   datasourceAddress=None, fields=None, expand=None):
    param_string = PySenseUtils.build_query_string({
        'parentFolder': parentFolder_id,
        'name': name,
        'datasourceTitle': datasourceTitle,
        'datasourceAddress': datasourceAddress,
        'fields': fields,
        'expand': expand
    })
    return PySenseDashboard.get_dashboards(param_string)


def get_dashboard_export_png(dashboard_id, path, param_dict):
    param_string = PySenseUtils.build_query_string(param_dict)
    return PySenseDashboard.get_dashboard_export_png(dashboard_id, path, param_string)


def get_dashboard_export_png(dashboard_id, path, includeTitle=None, includeFilters=None, includeDs=None, width=None):
    param_string = PySenseUtils.build_query_string({
        'includeTitle': includeTitle,
        'includeFilters': includeFilters,
        'includeDs': includeDs,
        'width': width
    })
    return PySenseDashboard.get_dashboard_export_png(dashboard_id, path, param_string)


def get_dashboard_export_pdf(dashboard_id, path, param_dict):
    # These are required parameters
    if 'paperFormat' in param_dict and 'paperOrientation' in param_dict and 'layout' in param_dict:
        param_string = PySenseUtils.build_query_string(param_dict)
        return PySenseDashboard.get_dashboard_export_pdf(dashboard_id, path, param_string)
    else:
        return None


def get_dashboard_export_pdf(dashboard_id, path, paperFormat, paperOrientation, layout):
    param_string = PySenseUtils.build_query_string({
        'paperFormat': paperFormat,
        'paperOrientation': paperOrientation,
        'layout': layout
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


############################################
# Helper Methods                           #
############################################

def get_folder_by_name(folder_name):
    folders = get_folders(name=folder_name)
    for folder in folders:
        if folder['name'] == folder_name:
            return folder
    return None


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

