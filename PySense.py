import requests
import config
import json
from collections import namedtuple


def _parse_error_response(response, error_text, exit_on_error=False):
    """
    Parses REST response object for errors

    :param response: the REST response object
    :param error_text: Text to print on error
    :param exit_on_error: True to exit on error, false to continue
    :return: True if no error, false if response errored

    """

    if response.status_code != 200:
        print("ERROR: {}: {}".format(error_text, response.status_code))
        print(response.content)
        if exit_on_error:
            exit()

        return False

    return True


def check_authentication():
    return {'host':config.host, 'token':config.token}


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
    resp = requests.post('{}/api/v1/authentication/login'.format(host), data=data)
    _parse_error_response(resp, "Error authenticating", True)

    access_code = "Bearer " + resp.json()['access_token']
    config.token = {'authorization': access_code}
    config.host = host
    return True


def _build_params(dict):
    ret_arr = []
    separator = '&'
    for key, value in dict.items():
        if value is not None:
            ret_arr.append("{}={}".format(key, value))
    return separator.join(ret_arr)


def get_dashboards(parentFolder=None, name=None, datasourceTitle=None, datasourceAddress=None, fields=None, expand=None):
    param_string = _build_params({
        'parentFolder': parentFolder,
        'name': name,
        'datasourceTitle': datasourceTitle,
        'datasourceAddress': datasourceAddress,
        'fields': fields,
        'expand': expand
    })
    resp = requests.get('{}/api/v1/dashboards?{}'.format(config.host, param_string), headers=config.token)
    ret_arr = []
    json_arr = resp.json()
    for json_obj in json_arr:
        json_obj['id'] = json_obj.pop('_id')
        ret_arr.append(namedtuple("Dashboard", json_obj.keys())(*json_obj.values()))

    return ret_arr


def get_dashboard_export_dash(dashboard_id, path):
    resp = requests.get('{}/api/v1/dashboards?{}'.format(config.host, dashboard_id), headers=config.token)
    with open(path, 'wb') as out_file:
        out_file.write(resp.content)
    return path


def get_dashboard_export_png(dashboard_id, path):
    resp = requests.get('{}/api/v1/dashboards?{}'.format(config.host, dashboard_id), headers=config.token)
    with open(path, 'wb') as out_file:
        out_file.write(resp.content)
    return path


def post_dashboards_import_bulk(dashboard, action=None, republish=None, importFolder=None):
    param_string = _build_params({
        'action': action,
        'republish': republish,
        'importFolder': importFolder
    })
    dashboard = "[" + dashboard + "]"
    print(requests.post('{}/api/v1/dashboards/import/bulk?{}'.format(config.host, param_string),
                        headers=config.token, json=json.loads(dashboard)).content)
