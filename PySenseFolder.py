import requests

import PySenseUtils
import PySenseConfig


def get_folders(param_string):
    resp = requests.get('{}/api/v1/folders?{}'.format(PySenseConfig.host, param_string), headers=PySenseConfig.token)
    if PySenseUtils.response_successful(resp):
        return resp.json()
    return None


def get_folders_id(folder_id):
    resp = requests.get('{}/api/v1/folders/{}'.format(PySenseConfig.host, folder_id), headers=PySenseConfig.token)
    if PySenseUtils.response_successful(resp):
        return resp.json()
    else:
        return None
