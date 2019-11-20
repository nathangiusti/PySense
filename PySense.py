import requests
import PySenseConfig
import json
from collections import namedtuple

############################################
# Utility methods #
############################################


def _response_successful(response):
    """
    Parses REST response object for errors

    :param response: the REST response object
    :return: True if no error, false if response errored
    """

    if response.status_code != 200:
        print("ERROR: {}: {}".format(response.status_code, response.content))
        print(response.content)
        return False
    return True


def _format_host(host):
    if not host.startswith('http'):
        host = 'http://' + host
    if host.endswith('/'):
        host = host[:-1]
    return host


def _build_query_string(dictionary):
    ret_arr = []
    separator = '&'
    for key, value in dictionary.items():
        if value is not None:
            ret_arr.append("{}={}".format(key, value))
    return separator.join(ret_arr)


############################################
# Authentication and configuration methods #
############################################

def set_host(host):
    """
    Set host manually. Host is automatically set when calling authenticate
    @param host: The new host
    @return: The host as it is set
    """
    config.host = _format_host(host)
    return config.host


def get_host():
    """

    @return: Returns the current host string
    """
    return config.host


def check_authentication():
    """
    Returns authentication parameters
    @return: A dictionary with an entry for host and token
    """
    return {'host': config.host, 'token': config.token}


def authenticate(host, username, password):
    """
    Authenticates with Sisense. Saves host and user token.

    :param host: the host address
    :param username: Username
    :param password: Password
    :return: True if successful, else false
    """

    data = {'username': username, 'password': password}

    resp = requests.post('{}/api/v1/authentication/login'.format(host), data=data)
    if _response_successful(resp):
        access_code = "Bearer " + resp.json()['access_token']
        config.token = {'authorization': access_code}
        config.host = _format_host(host)
        return True
    return False

############################################
# REST API wrappers                        #
############################################


def get_dashboards(param_dict):
    return _get_dashboards(_build_query_string(param_dict))


def get_dashboards(parentFolder=None, name=None, datasourceTitle=None,
                   datasourceAddress=None, fields=None, expand=None):
    param_string = _build_query_string({
        'parentFolder': parentFolder,
        'name': name,
        'datasourceTitle': datasourceTitle,
        'datasourceAddress': datasourceAddress,
        'fields': fields,
        'expand': expand
    })
    return _get_dashboards(param_string)


def _get_dashboards(param_string):
    resp = requests.get('{}/api/v1/dashboards?{}'.format(config.host, param_string), headers=config.token)
    if _response_successful(resp):
        ret_arr = []
        json_arr = resp.json()
        for json_obj in json_arr:
            json_obj['id'] = json_obj.pop('_id')
            ret_arr.append(namedtuple("Dashboard", json_obj.keys())(*json_obj.values()))
        return ret_arr
    return None


def get_dashboard_export_png(dashboard_id, path, param_dict):
    param_string = _build_query_string(param_dict)
    return _get_dashboard_export_png(dashboard_id, path, param_string)


def get_dashboard_export_png(dashboard_id, path, includeTitle=None, includeFilters=None, includeDs=None, width=None):
    param_string = _build_query_string({
        'includeTitle': includeTitle,
        'includeFilters': includeFilters,
        'includeDs': includeDs,
        'width': width
    })
    return _get_dashboard_export_png(dashboard_id, path, param_string)


def _get_dashboard_export_png(dashboard_id, path, param_string):
    resp = requests.get('{}/api/v1/dashboards/{}/export/png?{}'.format(config.host, dashboard_id, param_string),
                        headers=config.token)
    if _response_successful(resp):
        with open(path, 'wb') as out_file:
            out_file.write(resp.content)
        return path
    return None


def get_dashboard_export_pdf(dashboard_id, path, param_dict):
    # These are required parameters
    if 'paperFormat' in param_dict and 'paperOrientation' in param_dict and 'layout' in param_dict:
        param_string = _build_query_string(param_dict)
        return _get_dashboard_export_pdf(dashboard_id, path, param_string)
    else:
        return None


def get_dashboard_export_pdf(dashboard_id, path, paperFormat, paperOrientation, layout):
    param_string = _build_query_string({
        'paperFormat': paperFormat,
        'paperOrientation': paperOrientation,
        'layout': layout
    })
    return _get_dashboard_export_pdf(dashboard_id, path, param_string)


def _get_dashboard_export_pdf(dashboard_id, path, param_string):
    resp = requests.get('{}/api/v1/dashboards/{}/export/pdf?{}'.format(config.host, dashboard_id, param_string),
                        headers=config.token)
    if _response_successful(resp):
        with open(path, 'wb') as out_file:
            out_file.write(resp.content)
        return path
    return None


def post_dashboards_import_bulk(dashboard, param_dict):
    param_string = _build_query_string(param_dict)
    return _post_dashboards_import_bulk(dashboard, param_string)


def post_dashboards_import_bulk(dashboard, action=None, republish=None, importFolder=None):
    param_string = _build_query_string({
        'action': action,
        'republish': republish,
        'importFolder': importFolder
    })
    return _post_dashboards_import_bulk(dashboard, param_string)


def _post_dashboards_import_bulk(dashboard, param_string):
    dashboard = "[" + dashboard + "]"
    resp = requests.post('{}/api/v1/dashboards/import/bulk?{}'.format(config.host, param_string),
                         headers=config.token, json=json.loads(dashboard)).content
    return _response_successful(resp)


def post_dashboard_widget_export_png(dashboard_id, widget_id, path, param_dict):
    if 'width' in param_dict and 'height' in param_dict:
        param_string = _build_query_string(param_dict)
        return _post_dashboard_widget_export_png(dashboard_id, widget_id, path, param_string)
    else:
        return None


def post_dashboard_widget_export_png(dashboard_id, widget_id, path, width, height):
    param_string = _build_query_string({
        'width': width,
        'height': height
    })
    return _post_dashboard_widget_export_png(dashboard_id, widget_id, path, param_string)


def _post_dashboard_widget_export_png(dashboard_id, widget_id, path, param_string):
    resp = requests.get('{}/api/v1/dashboards/{}/widgets/{}/export/png?{}'.format(config.host, dashboard_id, widget_id, param_string), headers=config.token)
    if _response_successful(resp):
        with open(path, 'wb') as out_file:
            out_file.write(resp.content)
        return path
    else:
        return None


def get_dashboard_export_dash(dashboard, path):
    resp = requests.get('{}/api/v1/dashboards/{}/export/dash'.format(config.host, dashboard), headers=config.token)
    if _response_successful(resp):
        with open(path, 'wb') as out_file:
            out_file.write(resp.content)
        return path
    else:
        return None

