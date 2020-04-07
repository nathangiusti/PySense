import json
import requests

from PySense import PySenseUser


class RestError(Exception):
    pass


def parse_response(response):
    if response.status_code not in [200, 201, 204]:
        raise RestError('ERROR: {}: {}\nURL: {}'.format(response.status_code, response.content, response.url))

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
            validated = value
            if isinstance(value, bool):
                if value is True:
                    validated = 'true'
                elif value is False:
                    validated = 'false'
            elif isinstance(value, list):
                validated = ','.join(value)
            ret_arr.append("{}={}".format(key, validated))
    return separator.join(ret_arr)


def build_json_object(dictionary):
    ret_json = {}
    for key, value in dictionary.items():
        if value is not None:
            validated = value
            if isinstance(value, bool):
                if value is True:
                    validated = 'true'
                elif value is False:
                    validated = 'false'
            ret_json[key] = validated
    return ret_json


def get_user_id(host, token, email):
    resp = requests.get('{}/api/users?email={}'.format(host, email),
                        headers=token)
    parse_response(resp)
    for user in resp.json():
        if user['email'] == email:
            user = PySenseUser.User(host, token, user)
            return user.get_user_id()


def get_role_id(host, token, role_name):
    if role_name is None:
        return None
    resp = requests.get('{}/api/roles'.format(host),
                        headers=token)
    parse_response(resp)

    json_rep = json.loads(resp.content.decode('utf8'))
    for item in json_rep:
        if role_name == item['name'] or role_name == item['displayName']:
            return item['_id']
    raise Exception("Role with name {} not found".format(role_name))
