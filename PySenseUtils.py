from collections import namedtuple
import json
import requests
import PySenseConfig


def response_successful(response):
    """
    Parses REST response object for errors

    :param response: the REST response object
    :return: True if no error, false if response errored
    """

    if response is None:
        return None

    if response.status_code not in [200, 201, 204]:
        print("ERROR: {}: {}".format(response.status_code, response.content))
        print(response.content)
        return None
    return response


def format_host(host):
    if not host.startswith('http'):
        host = 'http://' + host
    if host.endswith('/'):
        host = host[:-1]
    return host


def build_query_string(dictionary):
    ret_arr = []
    separator = '&'
    for key, value in dictionary.items():
        if value is not None:
            ret_arr.append("{}={}".format(key, value))
    return separator.join(ret_arr)


def convert_to_named_tuple(title, json_obj):
    json_obj['id'] = json_obj.pop('_id')
    return namedtuple(title, json_obj.keys())(*json_obj.values())


def get_role_id(role_id):
    resp = requests.get('{}/api/roles'.format(PySenseConfig.host),
                        headers=PySenseConfig.token)
    json_rep = json.loads(resp.content.decode('utf8'))
    for item in json_rep:
        if role_id == item['_id'] or role_id == item['name'] or role_id == item['displayName']:
            return item['_id']
    return None


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


def get_user_id_by_email(email):
    resp = requests.get('{}/api/v1/users?email={}'.format(PySenseConfig.host, email),
                        headers=PySenseConfig.token)
    json_rep = json.loads(resp.content.decode('utf8'))
    if len(json_rep) == 1:
        return json_rep[0]['_id']
    else:
        print('{} users found with email address {}'.format(len(json_rep), email))
        return None
