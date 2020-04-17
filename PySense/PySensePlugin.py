import requests


class Plugin:

    def __init__(self, py_client, plugin_json):
        self._py_client = py_client
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
        resp_json = self._py_client.connector.rest_call('patch', 'api/v1/plugins', json_payload=[self._plugin_json])
        self._plugin_json = resp_json[0]
