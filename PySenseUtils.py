import json
import requests

def response_successful(response, success=None, failure=None):
    """
    Parses REST response object for errors

    :param response: the REST response object
    :param success: the object to return on success
    :param success: the object to return on failure
    :return: On success response or success if set, None or failure if response errored
    """

    if response is None:
        return failure

    if response.status_code not in [200, 201, 204]:
        print("ERROR: {}: {}".format(response.status_code, response.content))
        print(response.content)
        return failure

    if success:
        return success
    else:
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
    resp = requests.get('{}/api/roles'.format(host),
                        headers=token)
    if not response_successful(resp):
        return

    json_rep = json.loads(resp.content.decode('utf8'))
    for item in json_rep:
        if role_name == item['_id'] or role_name == item['name'] or role_name == item['displayName']:
            return item['_id']
    return None
