import requests
import config
import json
from collections import namedtuple


def set_host(host):
    config.host = host
    return config.host


def get_host():
    return config.host


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


def check_authentication():
    return {'host': config.host, 'token': config.token}


def authenticate(host, username, password):
    """
    Authenticates with Sisense

    :param host: the host address
    :param username: Username
    :param password: Password
    :return: A json blob to be used as a header for sisense calls
    """

    data = {'username': username, 'password': password}
    if not host.startswith('http://'):
        host = 'http://' + host
    if host.endswith('/'):
        host = host[:-1]
    resp = requests.post('{}/api/v1/authentication/login'.format(host), data=data)
    if _response_successful(resp):
        access_code = "Bearer " + resp.json()['access_token']
        config.token = {'authorization': access_code}
        config.host = host
        return True
    return False


def _build_params(dictionary):
    ret_arr = []
    separator = '&'
    for key, value in dictionary.items():
        if value is not None:
            ret_arr.append("{}={}".format(key, value))
    return separator.join(ret_arr)


def get_dashboards(param_dict=None, parentFolder=None, name=None, datasourceTitle=None, datasourceAddress=None, fields=None, expand=None):
    if param_dict:
        param_string = _build_params(param_dict)
    else:
        param_string = _build_params({
            'parentFolder': parentFolder,
            'name': name,
            'datasourceTitle': datasourceTitle,
            'datasourceAddress': datasourceAddress,
            'fields': fields,
            'expand': expand
        })
    resp = requests.get('{}/api/v1/dashboards?{}'.format(config.host, param_string), headers=config.token)
    if _response_successful(resp):
        ret_arr = []
        json_arr = resp.json()
        for json_obj in json_arr:
            json_obj['id'] = json_obj.pop('_id')
            ret_arr.append(namedtuple("Dashboard", json_obj.keys())(*json_obj.values()))
        return ret_arr
    return None


def get_dashboard_export_png(dashboard_id, path, param_dict=None, includeTitle=None, includeFilters=None, includeDs=None, width=None):
    if param_dict:
        param_string = _build_params(param_dict)
    else:
        param_string = _build_params({
            'includeTitle': includeTitle,
            'includeFilters': includeFilters,
            'includeDs': includeDs,
            'width': width
        })
    resp = requests.get('{}/api/v1/dashboards/{}/export/png?{}'.format(config.host, dashboard_id, param_string),
                        headers=config.token)
    if _response_successful(resp):
        with open(path, 'wb') as out_file:
            out_file.write(resp.content)
        return path
    return None


def get_dashboard_export_pdf(dashboard_id, path, paperFormat, paperOrientation, layout):
    param_string = _build_params({
        'paperFormat': paperFormat,
        'paperOrientation': paperOrientation,
        'layout': layout
    })
    resp = requests.get('{}/api/v1/dashboards/{}/export/pdf?{}'.format(config.host, dashboard_id, param_string),
                        headers=config.token)
    if _response_successful(resp):
        with open(path, 'wb') as out_file:
            out_file.write(resp.content)
        return path
    return None


def post_dashboards_import_bulk(dashboard, action=None, republish=None, importFolder=None):
    param_string = _build_params({
        'action': action,
        'republish': republish,
        'importFolder': importFolder
    })
    dashboard = "[" + dashboard + "]"
    resp = requests.post('{}/api/v1/dashboards/import/bulk?{}'.format(config.host, param_string),
                         headers=config.token, json=json.loads(dashboard)).content
    return _response_successful(resp)


def post_dashboard_widget_export_png(dashboard_id, widget_id, path, param_dict=None, width=None, height=None):
    param_string = None
    if param_dict:
        if 'width' in param_dict and 'height' in param_dict:
            param_string = _build_params(param_dict)

    if not param_string:
        if width is not None and height is not None:
            param_string = _build_params({
                'width': width,
                'height': height
            })
    if not param_string:
        print("No width or height given")
        return None

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

