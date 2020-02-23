import json
import requests


def parse_response(response):
    """
    Parses REST response object for errors

    :param response: the REST response object
    :return: The response object if no errors
    """

    if response.status_code not in [200, 201, 204]:
        raise Exception("ERROR: {}: {}".format(response.status_code, response.content))

    return response


def format_host(host):
    """
    Formats host string

    :param host: host
    :return: The formatted host string
    """
    if not host.startswith('http'):
        host = 'http://' + host
    if host.endswith('/'):
        host = host[:-1]
    return host


def build_query_string(dictionary):
    """
    Turns dictionary into param string

    :param dictionary: The dictionary of values to transform
    :return: A query string
    """
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
