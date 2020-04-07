import json
import requests

from PySense import PySenseUtils

class Widget:

    def __init__(self, host, token, widget_json):
        self._host = host
        self._token = token
        self._widget_json = widget_json

    def get_widget_json(self):
        """  
        Returns the widget's JSON  
          
        :return: The widget's JSON  
        """
        
        return self._widget_json
    
    def get_dashboard_id(self):
        """
        Returns the dashboard id of the widget  
         
        :return: The parent dashboard's dashboard id 
        """
        
        return self._widget_json['dashboardid']

    def get_id(self):
        """
        Gets the widget's id  
          
        :return: The widget's id  
        """
        
        return self._widget_json['oid']

    def export_to_png(self, width, height, *, path=None):
        """
        Export's widget to png  
        :param width: Render width in pixels  
        :param height: Render height in pixels   
          
        Optional:  
        :param path: Path to save the file  
           
        :return: The path of the saved file if set, else the raw content  
        """
        query_string = PySenseUtils.build_query_string({'width': width, 'height': height})
        resp = requests.get(
            '{}/api/v1/dashboards/{}/widgets/{}/export/png?{}'
            .format(self._host, self.get_dashboard_id(), self.get_id(), query_string), headers=self._token)
        PySenseUtils.parse_response(resp)
        if path is not None:
            with open(path, 'wb') as out_file:
                out_file.write(resp.content)
            return path
        else:
            return resp.content
