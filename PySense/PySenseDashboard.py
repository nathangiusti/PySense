import json
import requests

from PySense import PySenseUtils
from PySense import PySenseWidget


class Dashboard:

    def __init__(self, host, token, dashboard_json):
        self._host = host
        self._token = token
        self._dashboard_json = dashboard_json

    def _reset(self, dashboard_json):
        self._dashboard_json = dashboard_json

    def get_id(self):
        """
        Gets the dashboard's id 
  
        :return: The dashboard's id  
        """
        
        return self._dashboard_json['oid']

    def get_name(self):
        """
        Gets the dashboard's title  
  
        :return: The dashboards title   
        """
        
        return self._dashboard_json['title']

    def get_dashboard_folder_id(self):
        """
        Gets the dashboards folder id  
  
        :return: The folder id of the parent folder of the dashboard  
        """
        
        return self._dashboard_json['parentFolder']

    def get_shares(self):
        """
        Gets the dashboard shares json  
  
        :return: The dashboard shares json  
        """

        resp = requests.get(
            '{}/api/shares/dashboard/{}'.format(self._host, self.get_id()),
            headers=self._token)
        PySenseUtils.parse_response(resp)
        return resp.json()

    def move_to_folder(self, folder):
        """
        Move dashboard to given folder  
  
        :param folder: Folder object to move dashboard to, None to remove from folder  
        
        :return: True if successful  
        """
        if folder:
            folder_oid = folder.get_folder_id()
        else:
            folder_oid = None
        resp = requests.patch(
            '{}/api/v1/dashboards/{}'.format(self._host, self.get_id()),
            headers=self._token, json={'parentFolder': folder_oid})
        PySenseUtils.parse_response(resp)
        self._reset(resp.json())
        return True

    def share_to_user(self, email, rule, subscribe):
        """
        Share a dashboard to a user  
  
        :param email: The email address of the user  
        :param rule: The permission of the user on the dashboard (view, edit, etc)  
        :param subscribe: true or false, whether to subscribe the user to reports  
          
        :return: The updated share  
        """

        user_id = PySenseUtils.get_user_id(self._host, self._token, email)
        shares = self.get_shares()
        shares['sharesTo'].append({'shareId': user_id, 'type': 'user', 'rule': rule, 'subscribe': subscribe})
        resp = requests.post(
            '{}/api/shares/dashboard/{}'.format(self._host, self.get_id()),
            headers=self._token, json=shares)
        PySenseUtils.parse_response(resp)
        return self.get_shares()

    def unshare_to_user(self, email):
        """
        Unshare a dashboard to a user  
  
        :param email: The email address of the user  
           
        :return: The updated share  
        """

        shares = self.get_shares()
        for i, share in enumerate(shares['sharesTo']):
            if share['email'] == email:
                del shares['sharesTo'][i]
        resp = requests.post(
            '{}/api/shares/dashboard/{}'.format(self._host, self.get_id()),
            headers=self._token, json=shares)
        PySenseUtils.parse_response(resp)
        return self.get_shares()

    def export_to_png(self, *, path=None, include_title=None, include_filters=None, include_ds=None, width=None):
        """
        Get dashboard as png    
  
        Optional:
        :param path: Path to save location of png    
        :param include_title: Should dashboard title be included in the exported file  
        :param include_filters: Should dashboard filters be included in the exported file  
        :param include_ds: Should dashboard data source info be included in the exported file  
        :param width: Render width in pixels  
          
        :return: The path of the created file if provided or else the raw response obejct  
        """
        
        param_string = PySenseUtils.build_query_string({
            'includeTitle': include_title,
            'includeFilters': include_filters,
            'includeDs': include_ds,
            'width': width
        })
        resp = requests.get(
            '{}/api/v1/dashboards/{}/export/png?{}'.format(self._host, self.get_id(), param_string),
            headers=self._token)
        PySenseUtils.parse_response(resp)
        if path is not None:
            with open(path, 'wb') as out_file:
                out_file.write(resp.content)
            return path
        else: 
            return resp.content

    def export_to_pdf(self, paper_format, paper_orientation, layout, *, path=None,
                      include_title=None, include_filters=None, include_ds=None, widget_id=None,
                      preview=None,
                      row_count=None, show_title=None, show_footer=None, title=None, title_size=None,
                      title_position=None):
        """
        Get dashboard as pdf  
  
        :param paper_format: What paper format should be used while rendering the dashboard.  
        :param paper_orientation: What paper orientation should be used while rendering the dashboard  
        :param layout: What layout should be used while rendering the dashboard, as is or feed  
        
        Optional:
        :param path: Path to save location of pdf  
        :param include_title: Should dashboard title be included in the exported file  
        :param include_filters: Should dashboard filters be included in the exported file  
        :param include_ds: Should dashboard datasource info be included in the exported file  
        :param widget_id: Widget Id (Use only for Table and Pivot Widgets)  
        :param preview: Should use a new Pixel Perfect Reporting  
        :param row_count: Count of Table/Pivot rows to export  
        :param show_title: Should Table/Pivot Widget title be included in the exported file  
        :param show_footer: Should Table/Pivot Widget footer be included in the exported file  
        :param title: Table/Pivot Widget title text in the exported file  
        :param title_size: Table/Pivot widget title size in the exported file  
        :param title_position: Table/Pivot widget title position in the exported file  
        :return: The path of the created file if provided, else the raw content
        """
        
        param_string = PySenseUtils.build_query_string({
            'paperFormat': paper_format,
            'paperOrientation': paper_orientation,
            'layout': layout,
            'includeTitle': include_title,
            'includeFilters': include_filters,
            'includeDs': include_ds,
            'widgetid': widget_id,
            'preview': preview,
            'rowCount': row_count,
            'showTitle': show_title,
            'showFooter': show_footer,
            'title': title,
            'titleSize': title_size,
            'titlePosition': title_position
        })
        resp = requests.get('{}/api/v1/dashboards/{}/export/pdf?{}'
                            .format(self._host, self.get_id(), param_string), headers=self._token)
        PySenseUtils.parse_response(resp)
        if path is not None:
            with open(path, 'wb') as out_file:
                out_file.write(resp.content)
            return path
        else:
            return resp.content

    def export_to_dash(self, *, path=None):
        """
        Get dashboard as dash file  
  
        Optional:
        :param path: Path to save location of dash file  
        
        :return: The path of the created file if path provided, else the raw content
        """
        
        resp = requests.get('{}/api/v1/dashboards/{}/export/dash'.format(self._host, self.get_id()),
                            headers=self._token)
        PySenseUtils.parse_response(resp)
        if path is not None:
            with open(path, 'wb') as out_file:
                out_file.write(resp.content)
            return path
        else:
            return resp.content

    def get_widgets(self, *, title=None, type=None, subtype=None,
                    fields=None, sort=None, skip=None, limit=None):
        """
        Returns an array of a dashboard’s widgets.  
  
        Optional:
        :param title: Widget title to filter by  
        :param type: Widget type to filter by  
        :param subtype: Widget sub-type to filter by  
        :param fields: Whitelist of fields to return for each document. fields Can also define which fields to exclude  
            by prefixing field names with -  
        :param sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -  
        :param skip: Number of results to skip from the start of the data set. skip is to be used with the limit  
            parameter for paging  
        :param limit: How many results should be returned. limit is to be used with the skip parameter for paging  
          
        :return: An array of widget objects  
        """
        
        param_string = PySenseUtils.build_query_string({
            'title': title,
            'type': type,
            'subtype': subtype,
            'fields': fields,
            'sort': sort,
            'skip': skip,
            'limit': limit
        })

        resp = requests.get(
            '{}/api/v1/dashboards/{}/widgets?{}'.format(self._host, self.get_id(), param_string),
            headers=self._token)

        PySenseUtils.parse_response(resp)
        ret_arr = []
        widgets_json = json.loads(resp.content)
        for widget in widgets_json:
            ret_arr.append(PySenseWidget.Widget(self._host, self._token, widget))
        return ret_arr

    def get_widget_by_id(self, widget_id, *, fields=None):
        """
        Returns a specific widget (by ID) from a specific dashboard.  
    
        :param widget_id: The ID of the widget to get   
           
        Optional:  
        :param fields: Whitelist of fields to return for each document. fields Can also define which fields to exclude  
            by prefixing field names with -  
            
        :return: A widget object  
        """
        
        param_string = PySenseUtils.build_query_string({
            'fields': fields
        })

        resp = requests.get('{}/api/v1/dashboards/{}/widgets/{}?{}'.format(self._host, self.get_id(),
                                                                           widget_id, param_string),
                            headers=self._token)
        PySenseUtils.parse_response(resp)
        return PySenseWidget.Widget(self._host, self._token, json.loads(resp.content))

    def add_widget(self, widget):
        """
        Adds the provided widget object to the dashboard  

        :param widget: widget object to add  
        
        :return: The widget added to the dashboard  
        """
        
        resp = requests.post('{}/api/v1/dashboards/{}/widgets'.format(self._host, self.get_id()),
                             headers=self._token, json=widget.get_widget_json())
        PySenseUtils.parse_response(resp)
        return PySenseWidget.Widget(self._host, self._token, json.loads(resp.content))

    def delete_widget(self, widget_id):
        """  
        Deletes a widget with the provided ID from it’s dashboard.  
  
        :param widget_id: The ID of the widget to delete  
        """  
        
        resp = requests.delete('{}/api/v1/dashboards/{}/widgets/{}'
                               .format(self._host, self.get_id(), widget_id), headers=self._token)
        PySenseUtils.parse_response(resp)
        # Get the updated dashboard from source and refresh object
        resp = requests.get('{}/api/v1/dashboards/{}'.format(self._host, self.get_id()),
                            headers=self._token)
        PySenseUtils.parse_response(resp)
        self._reset(resp.json())

    def does_widget_exist(self, widget_id):  
        """
        Returns whether or not a widget with the given id is in the dashboard  
          
        :param widget_id: The widget id to look for  
          
        :return: True if found, false if not.  
        """
         
        try:
            self.get_widget_by_id(widget_id)
        except PySenseUtils.RestError:
            return False
        else:
            return True

    def remove_ghost_widgets(self):
        """
        Removes ghost widgets from dashboard  
        """
        
        patch_json = {"layout": self._dashboard_json['layout']}
        modified = True
        while modified:
            modified = False
            for l, column in enumerate(patch_json['layout']['columns']):
                for k, cell in enumerate(column['cells']):
                    for j, sub_cell in enumerate(cell['subcells']):
                        for i, element in enumerate(sub_cell['elements']):
                            if not self.does_widget_exist(element['widgetid']):
                                sub_cell['elements'].pop(i)
                                modified = True
                        if len(sub_cell['elements']) == 0:
                            cell['subcells'].pop(j)
                    if len(cell['subcells']) == 0:
                        column['cells'].pop(k)
                if len(column['cells']) == 0:
                    patch_json['layout']['columns'].pop(l)
        resp = requests.patch('{}/api/v1/dashboards/{}'.format(self._host, self.get_id()),
                              headers=self._token, json=patch_json)
        PySenseUtils.parse_response(resp)
        self._reset(resp.json())
