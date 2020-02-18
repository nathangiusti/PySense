import requests
import PySenseUtils
import json


class Dashboard:
    host = None
    token = None
    dashboard_json = None

    def __init__(self, host, token, dashboard_json):
        self.host = host
        self.token = token
        self.dashboard_json = dashboard_json
        self.dashboard_id = dashboard_json['oid']

    def get_dashboard_id(self):
        return self.dashboard_id

    def get_dashboard_title(self):
        return self.dashboard_json['title']

    def get_dashboard_json(self):
        return self.dashboard_json

    def get_dashboard_export_png(self, path, includeTitle=None, includeFilters=None, includeDs=None, width=None):
        """
         Get dashboard as png

         :param path: Path to save location of png
         :param includeTitle: Should dashboard title be included in the exported file
         :param includeFilters: Should dashboard filters be included in the exported file
         :param includeDs: Should dashboard datasource info be included in the exported file
         :param width: Render width in pixels
         :return: The path of the created file or None on error
         """
        param_string = PySenseUtils.build_query_string({
            'includeTitle': includeTitle,
            'includeFilters': includeFilters,
            'includeDs': includeDs,
            'width': width
        })
        resp = requests.get(
            '{}/api/v1/dashboards/{}/export/png?{}'.format(self.host, self.get_dashboard_id(), param_string),
            headers=self.token)
        if PySenseUtils.response_successful(resp):
            with open(path, 'wb') as out_file:
                out_file.write(resp.content)
            return path
        return None

    def get_dashboard_export_pdf(self, path, paperFormat, paperOrientation, layout,
                                 includeTitle=None, includeFilters=None, includeDs=None, widgetid=None, preview=None,
                                 rowCount=None, showTitle=None, showFooter=None, title=None, titleSize=None,
                                 titlePosition=None):
        """
        Get dashboard as pdf

        :param path: Path to save location of pdf
        :param paperFormat: What paper format should be used while rendering the dashboard.
        :param paperOrientation: What paper orientation should be used while rendering the dashboard
        :param layout: What layout should be used while rendering the dashboard, as is or feed
        :param includeTitle: Should dashboard title be included in the exported file
        :param includeFilters: Should dashboard filters be included in the exported file
        :param includeDs: Should dashboard datasource info be included in the exported file
        :param widgetid: Widget Id (Use only for Table and Pivot Widgets)
        :param preview: Should use a new Pixel Perfect Reporting
        :param rowCount: Count of Table/Pivot rows to export
        :param showTitle: Should Table/Pivot Widget title be included in the exported file
        :param showFooter: Should Table/Pivot Widget footer be included in the exported file
        :param title: Table/Pivot Widget title text in the exported file
        :param titleSize: Table/Pivot widget title size in the exported file
        :param titlePosition: Table/Pivot widget title position in the exported file
        :return: The path of the created file or None on error
        """
        param_string = PySenseUtils.build_query_string({
            'paperFormat': paperFormat,
            'paperOrientation': paperOrientation,
            'layout': layout,
            'includeTitle': includeTitle,
            'includeFilters': includeFilters,
            'includeDs': includeDs,
            'widgetid': widgetid,
            'preview': preview,
            'rowCount': rowCount,
            'showTitle': showTitle,
            'showFooter': showFooter,
            'title': title,
            'titleSize': titleSize,
            'titlePosition': titlePosition
        })
        resp = requests.get('{}/api/v1/dashboards/{}/export/pdf?{}'
                            .format(self.host, self.get_dashboard_id(), param_string), headers=self.token)
        if PySenseUtils.response_successful(resp):
            with open(path, 'wb') as out_file:
                out_file.write(resp.content)
            return path
        return None

    def get_dashboard_export_dash(self, path):
        """
        Get dashboard as pdf

        :param path: Path to save location of dash file
        :return: The path of the created file or None on error
        """
        resp = requests.get('{}/api/v1/dashboards/{}/export/dash'.format(self.host, self.get_dashboard_id()),
                            headers=self.token)
        if PySenseUtils.response_successful(resp):
            with open(path, 'wb') as out_file:
                out_file.write(resp.content)
            return path
        else:
            return None

    def post_dashboard_widget_export_png(self, widget_id, path, width, height):
        param_string = PySenseUtils.build_query_string({
            'width': width,
            'height': height
        })
        resp = requests.get(
            '{}/api/v1/dashboards/{}/widgets/{}/export/png?{}'.format(self.host, self.get_dashboard_id(), widget_id,
                                                                      param_string), headers=self.token)
        if PySenseUtils.response_successful(resp):
            with open(path, 'wb') as out_file:
                out_file.write(resp.content)
            return path
        else:
            return None

    def get_dashboards_widget(self, widget_id):
        resp = requests.get('{}/api/v1/dashboards/{}/widgets/{}'.format(self.host, self.get_dashboard_id(), widget_id),
                            headers=self.token)
        return PySenseUtils.response_successful(resp, success=resp.content)

    def get_dashboards_widgets(self):
        resp = requests.get('{}/api/v1/dashboards/{}/widgets'.format(self.host, self.get_dashboard_id()),
                            headers=self.token)
        return PySenseUtils.response_successful(resp, success=resp.content)

    def post_dashboards_widgets(self, widget):
        widget_str = widget.decode("utf-8")
        resp = requests.post('{}/api/v1/dashboards/{}/widgets'.format(self.host, self.get_dashboard_id()),
                             headers=self.token, json=json.loads(widget_str))
        return PySenseUtils.response_successful(resp)

    def delete_dashboards_widgets(self, widget_id):
        resp = requests.delete('{}/api/v1/dashboards/{}/widgets/{}'
                               .format(self.host,  self.get_dashboard_id(), widget_id), headers=self.token)
        return PySenseUtils.response_successful(resp)
