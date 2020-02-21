import requests
import PySenseUtils
import json
import PySenseWidget


class Dashboard:

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
        Get dashboard as dash file

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

    def get_dashboard_widgets(self, title=None, type=None, subtype=None,
                              fields=None, sort=None, skip=None, limit=None):
        """
        Returns an array of a dashboard’s widgets.

        @param title: Widget title to filter by
        @param type: Widget type to filter by
        @param subtype: Widget sub-type to filter by
        @param fields: Whitelist of fields to return for each document. fields Can also define which fields to exclude
            by prefixing field names with -
        @param sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -
        @param skip: Number of results to skip from the start of the data set. skip is to be used with the limit
            parameter for paging
        @param limit: How many results should be returned. limit is to be used with the skip parameter for paging
        @return: An array of widget objects or None on error
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
            '{}/api/v1/dashboards/{}/widgets?{}'.format(self.host, self.get_dashboard_id(), param_string),
            headers=self.token)

        if PySenseUtils.response_successful(resp):
            ret_arr = []
            widgets_json = json.loads(resp.content)
            for widget in widgets_json:
                ret_arr.append(PySenseWidget.Widget(self.host, self.token, widget))
            return ret_arr
        else:
            return None

    def get_dashboards_widget_by_id(self, widget_id, fields=None):
        """
        Returns a specific widget (by ID) from a specific dashboard.

        @param widget_id: The ID of the widget to get
        @param fields: Whitelist of fields to return for each document. fields Can also define which fields to exclude
            by prefixing field names with -
        @return: A widget object or None on error
        """
        param_string = PySenseUtils.build_query_string({
            'fields': fields
        })

        resp = requests.get('{}/api/v1/dashboards/{}/widgets/{}?{}'.format(self.host, self.get_dashboard_id(),
                                                                           widget_id, param_string),
                            headers=self.token)
        return PySenseUtils.response_successful(resp, success=PySenseWidget.Widget(
            self.host, self.token, json.loads(resp.content)))

    def post_dashboards_widgets(self, widget):
        """
        Adds the provided widget object to the dashboard

        @param widget: widget object to add
        @return: The widget added to the dashboard or None on error
        """
        resp = requests.post('{}/api/v1/dashboards/{}/widgets'.format(self.host, self.get_dashboard_id()),
                             headers=self.token, json=widget.get_widget_json())
        return PySenseUtils.response_successful(resp, success=PySenseWidget.Widget(
            self.host, self.token, json.loads(resp.content)))

    def delete_dashboards_widgets(self, widget_id):
        """
        Deletes a widget with the provided ID from it’s dashboard.

        @param widget_id: The ID of the widget to delete
        @return: Response object if successful, None on error
        """
        resp = requests.delete('{}/api/v1/dashboards/{}/widgets/{}'
                               .format(self.host,  self.get_dashboard_id(), widget_id), headers=self.token)
        return PySenseUtils.response_successful(resp)
