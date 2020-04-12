import requests
import urllib.parse

from PySense import PySenseException
from PySense import PySenseFolder
from PySense import PySenseGroup
from PySense import PySenseUser


class RestConnector:
    
    def __init__(self, host, username, password, debug):
        self._host = format_host(host)
        self.debug = debug
        data = {'username': username, 'password': password}
        resp = requests.post('{}/api/v1/authentication/login'.format(self._host), data=data)
        parse_response(resp)
        self._token = {'authorization':  "Bearer " + resp.json()['access_token']}
        self._roles = self.rest_call('get', 'api/roles')
        
    def rest_call(self, action_type, url, *, data=None, json_payload=None, query_params=None, raw=False):
        """
        Run an arbitrary rest command against your Sisense instance and returns the JSON response    
    
        :param action_type: REST request type  
        :param url: url to hit, example api/v1/app_database/encrypt_database_password or api/branding  
        
        Optional:  
        :param data: The data portion of the payload  
        :param json_payload: The json portion of the payload  
        :param query_params: a dictionary of query values to be added to the end of the url  
        :param raw: True if raw content response wanted, 
        :return: The rest response object  
        """
        
        action_type = action_type.lower()
        if query_params is not None:
            query_string = build_query_string(query_params)
        else:
            query_string = ''
        full_url = '{}/{}{}'.format(self._host, url, query_string)

        if self.debug:
            print('{}: {}'.format(action_type, full_url))
            if data is not None:
                print('Data: {}'.format(data))
            if json_payload is not None:
                print('JSON: {}'.format(json_payload))
        response = requests.request(action_type, full_url, headers=self._token, data=data, json=json_payload)
        parse_response(response)
        if len(response.content) == 0:
            return None
        elif raw:
            return response.content
        else:
            try:
                return response.json()
            except ValueError as e:
                return response.content
            
    def get_role_id(self, role_name):
        """
        Get the role id for the given role name  

        :param role_name: The role name

        :return: The role id  
        """
        if role_name is None:
            return None
        for item in self._roles:
            if role_name == item['name'] or role_name == item['displayName']:
                return item['_id']
        raise PySenseException.PySenseException('No role with name {} found'.format(role_name))
            
    def get_role_name(self, role_id):
        """
        Get the role name for the given role id  

        :param role_id: The role name

        :return: The role name 
        """
        
        for item in self._roles:
            if role_id == item['_id']:
                return item['displayName']
        raise PySenseException.PySenseException('No role with id {} found'.format(role_id))
    
    def get_user_by_email(self, email):
        query_params = {'email': email}
        resp_json = self.rest_call('get', 'api/v1/users', query_params=query_params)
        if len(resp_json) == 0:
            raise PySenseException.PySenseException('No user with email {} found'.format(email))
        elif len(resp_json) > 1:
            raise PySenseException.PySenseException('{} users with email {} found. '.format(len(resp_json), email))
        else:
            return PySenseUser.User(self, resp_json[0])

    def get_folder_by_id(self, folder_id):
        """  
        Get a specific folder by folder id  

        :param folder_id: The folder id of the folder  

        :return: A PySense folder object of the folder or None if not in a folder  
        """
        if folder_id is None:
            return None
        resp_json = self.rest_call('get', 'api/v1/folders/{}'.format(folder_id))
        return PySenseFolder.Folder(self, resp_json)
    
    def get_group_by_id(self, group_id):
        """
        Get a group by id
        
        :param group_id: The id of the group  
        
        :return: The PySense group   
        """
        
        resp_json = self.rest_call('get', 'api/groups/{}'.format(group_id))
        return PySenseGroup.Group(self, resp_json)


def parse_response(response):
    if response.status_code not in [200, 201, 204]:
        raise PySenseException.PySenseException('ERROR: {}: {}\nURL: {}'
                                                .format(response.status_code, response.content, response.url))


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
            if isinstance(value, bool):
                if value is True:
                    validated = 'true'
                elif value is False:
                    validated = 'false'
            elif isinstance(value, list):
                validated = ','.join(value)
            else:
                validated = urllib.parse.quote(str(value))
            ret_arr.append("{}={}".format(key, validated))
    query_string = separator.join(ret_arr)
    if len(query_string) > 1:
        return '?' + query_string
    else:
        return ''






