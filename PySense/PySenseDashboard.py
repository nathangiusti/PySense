from PySense import PySenseGroup
from PySense import PySenseException
from PySense import PySenseUser
from PySense import PySenseUtils
from PySense import PySenseWidget


class Dashboard:

    def __init__(self, connector, dashboard_json):
        self._dashboard_json = dashboard_json
        self._connector = connector
        
    def _reset(self):
        self._dashboard_json = self._connector.rest_call('get', 'api/v1/dashboards/{}'.format(self.get_id()))

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

    def get_dashboard_folder(self):
        """
        Gets the dashboards folder
  
        :return: The folder of the parent folder of the dashboard  
        """
        
        return self._connector.get_folder_by_id(self._dashboard_json['parentFolder'])

    def get_shares(self):
        """
        Gets the dashboard shares json  
  
        :return: The dashboard shares json  
        """
        resp_json = self._connector.rest_call('get', 'api/shares/dashboard/{}'.format(self.get_id()))
        return_json = {'sharesTo': []}
        for share in resp_json['sharesTo']:
            share_json = {
                'shareId': share['shareId'], 
                'type': share['type']
            }
            if 'rule' in share:
                share_json['rule'] = share['rule']
            if 'subscribe' in share:
                share_json['subscribe'] = share['subscribe']
            return_json['sharesTo'].append(share_json)
        return return_json

    def move_to_folder(self, folder):
        """
        Move dashboard to given folder  
  
        :param folder: Folder object to move dashboard to, None to remove from folder  
        """
        if folder:
            folder_oid = folder.get_id()
        else:
            folder_oid = None
        self._connector.rest_call('patch', 'api/v1/dashboards/{}'.format(self.get_id()), 
                                  json_payload={'parentFolder': folder_oid})
        self._reset()

    def add_shares(self, share, rule, subscribe):
        """
        Share a dashboard to a new group or user  
  
        :param share: A PySense Group or User
        :param rule: The permission of the user on the dashboard (view, edit, etc)  
        :param subscribe: true or false, whether to subscribe the user to reports    
        """
        curr_shares = self.get_shares()
        if isinstance(share, PySenseUser.User):
            curr_shares['sharesTo'].append(
                {'shareId': share.get_id(), 'type': 'user', 'rule': rule, 'subscribe': subscribe}
            )
        elif isinstance(share, PySenseGroup.Group):
            curr_shares['sharesTo'].append(
                {'shareId': share.get_id(), 'type': 'group', 'rule': rule, 'subscribe': subscribe}
            )
        
        self._connector.rest_call('post', 'api/shares/dashboard/{}'.format(self.get_id()), json_payload=curr_shares)
        
    def remove_shares(self, shares):
        """
        Unshare a dashboard to a listed groups and users
  
        :param shares: One to many groups and users to remove  
        """
        
        share_ids_to_delete = []
        for shares in PySenseUtils.make_iterable(shares):
            share_ids_to_delete.append(shares.get_id())
        current_shares = self.get_shares()
        for share_id in share_ids_to_delete:
            for i, shares in enumerate(current_shares['sharesTo']):
                if shares['shareId'] == share_id:
                    del current_shares['sharesTo'][i]
        
        self._connector.rest_call('post', 'api/shares/dashboard/{}'.format(self.get_id()), json_payload=current_shares)

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
        
        query_params = {
            'includeTitle': include_title,
            'includeFilters': include_filters,
            'includeDs': include_ds,
            'width': width
        }
        resp_content = self._connector.rest_call('get', 'api/v1/dashboards/{}/export/png'.format(self.get_id()), 
                                                 query_params=query_params, raw=True),
        if path is not None:
            with open(path, 'wb') as out_file:
                out_file.write(resp_content)
            return path
        else: 
            return resp_content

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
        
        query_params = {
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
        }
        resp_content = self._connector.rest_call('get', 'api/v1/dashboards/{}/export/pdf'.format(self.get_id()), 
                                                 query_params=query_params)

        if path is not None:
            with open(path, 'wb') as out_file:
                out_file.write(resp_content)
            return path
        else: 
            return resp_content

    def export_to_dash(self, *, path=None):
        """
        Get dashboard as dash file   
   
        Optional:  
        :param path: Path to save location of dash file  
        
        :return: The path of the created file if path provided, else the raw content  
        """
        
        resp_content = self._connector.rest_call('get', 'api/v1/dashboards/{}/export/dash'.format(self.get_id()), 
                                                 raw=True)
        if path is not None:
            with open(path, 'wb') as out_file:
                out_file.write(resp_content)
            return path
        else: 
            return resp_content

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
        
        query_params = {
            'title': title,
            'type': type,
            'subtype': subtype,
            'fields': fields,
            'sort': sort,
            'skip': skip,
            'limit': limit
        }
        
        ret_arr = []
        resp_json = self._connector.rest_call('get', 'api/v1/dashboards/{}/widgets'.format(self.get_id()),
                                              query_params=query_params)
        for widget in resp_json:
            ret_arr.append(PySenseWidget.Widget(self._connector, widget))
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
        
        query_params = {
            'fields': fields
        }

        resp_json = self._connector.rest_call('get', 'api/v1/dashboards/{}/widgets/{}'.format(self.get_id(), widget_id), 
                                              query_params=query_params),
        return PySenseWidget.Widget(self._connector, resp_json[0])

    def add_widget(self, widget):
        """
        Adds the provided widget object to the dashboard  

        :param widget: widget object to add  
        
        :return: The widget added to the dashboard  
        """
        
        resp_json = self._connector.rest_call('post', 'api/v1/dashboards/{}/widgets'.format(self.get_id()), 
                                              json_payload=widget.get_widget_json())
        return PySenseWidget.Widget(self._connector, resp_json)

    def delete_widget(self, widget_id):
        """  
        Deletes a widget with the provided ID from it’s dashboard.  
  
        :param widget_id: The ID of the widget to delete  
        """  
        
        self._connector.rest_call('delete', 'api/v1/dashboards/{}/widgets/{}'.format(self.get_id(), widget_id))
        self._reset()

    def remove_ghost_widgets(self):
        """
        Removes ghost widgets from dashboard  
        """
        
        patch_json = {"layout": self._dashboard_json['layout']}
        modified = True
        while modified:
            modified = False
            for n, column in enumerate(patch_json['layout']['columns']):
                for k, cell in enumerate(column['cells']):
                    for j, sub_cell in enumerate(cell['subcells']):
                        for i, element in enumerate(sub_cell['elements']):
                            if not self._does_widget_exist(element['widgetid']):
                                sub_cell['elements'].pop(i)
                                modified = True
                        if len(sub_cell['elements']) == 0:
                            cell['subcells'].pop(j)
                    if len(cell['subcells']) == 0:
                        column['cells'].pop(k)
                if len(column['cells']) == 0:
                    patch_json['layout']['columns'].pop(n)
        self._connector.rest_call('patch', 'api/v1/dashboards/{}'.format(self.get_id()), json_payload=patch_json)
        self._reset()
        
    def _does_widget_exist(self, widget_id):
        try:
            self.get_widget_by_id(widget_id)
        except PySenseException.PySenseException:
            return False
        else:
            return True
