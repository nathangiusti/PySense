import requests

from PySense import PySenseUtils


class Plugin:

    def __init__(self, host, token, plugin_json):
        self._host = host
        self._token = token
        self._plugin_json = plugin_json
    
    def get_name(self):
        """
        Get the plugins name  
          
        :return: The plugins name  
        """
        return self._plugin_json['name']

    def get_last_update(self):
        """
        Get the plugins last update  
  
        :return: The plugins last update  
        """
        return self._plugin_json['lastUpdate']
    
    def get_version(self):
        """
        Get the plugins version  

        :return: The plugins version  
        """
        return self._plugin_json['version']

    def get_is_enabled(self):
        """
        Returns whether the plugin is enabled    
  
        :return: True or false as to whether plugin is enabled
        """
        return self._plugin_json['isEnabled']

    def set_plugin_enabled(self, enabled):
        """
        Enable/disable the plugin
        
        :param enabled: True to enable, false to disable 
        """
        self._plugin_json['isEnabled'] = enabled
        resp = requests.patch('{}/api/v1/plugins'.format(self._host), headers=self._token, json=[self._plugin_json])
        PySenseUtils.parse_response(resp)
        self._plugin_json = resp.json()[0]
