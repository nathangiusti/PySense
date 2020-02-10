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




