import requests
import yaml

from PySense import PySense
from PySense import PySenseException
from PySense import PySenseUtils


def generate_token(host, username, password, verify=True):
    """Creates a new PySense client with the username and password

    Args:
        host (str): The Sisense server address
        username (str): Sisense username
        password (str): Sisense password
        verify (bool): SSL Verification

    Returns:
        JSON: A json authorization header
    """

    host = PySenseUtils.format_host(host)
    data = {'username': username, 'password': password}
    resp = requests.post('{}/api/v1/authentication/login'.format(host), verify=verify, data=data)
    if resp.status_code not in [200, 201, 204]:
        raise PySenseException.PySenseException('ERROR: {}: {}\nURL: {}'
                                                .format(resp.status_code, resp.content, resp.url))
    return {'authorization':  "Bearer " + resp.json()['access_token']}


def authenticate_by_token(host, token, version, debug=False, verify=True, param_dict=None):
    """Do not call directly. Call from PySense"""

    host = PySenseUtils.format_host(host)
    token_json = {'authorization':  "Bearer " + token}
    return PySense.PySense(host, token_json, version, debug=debug, verify=verify, param_dict=param_dict)


def authenticate_by_password(host, username, password, version, debug=False, verify=True, param_dict=None):
    """Do not call directly. Call from PySense"""

    host = PySenseUtils.format_host(host)
    token = generate_token(host, username, password, verify=verify)
    return PySense.PySense(host, token, version, debug=debug, verify=verify, param_dict=param_dict)


def authenticate_by_file(config_file):
    """Do not call directly. Call from PySense"""

    with open(config_file, 'r') as yml_file:
        cfg = yaml.safe_load(yml_file)

        debug = cfg['debug'] if 'debug' in cfg else False
        verify = cfg['verify'] if 'verify' in cfg else True
        token = cfg['token'] if 'token' in cfg else None
        host = PySenseUtils.format_host(cfg['host'])
        if token is None:
            return authenticate_by_password(host, cfg['username'], cfg['password'], cfg['version'],
                                            debug=debug, verify=verify, param_dict=cfg)
        else:
            return authenticate_by_token(host, cfg['token'], cfg['version'], debug=debug, verify=verify, param_dict=cfg)

