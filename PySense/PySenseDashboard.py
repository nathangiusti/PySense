import json
import requests

from PySense import PySenseUtils
from PySense import PySenseWidget


class Dashboard:

    def __init__(self, host, token, dashboard_json):
        self._host = host
        self._token = token
        self._dashboard_json = dashboard_json
        self._dashboard_id = dashboard_json['oid']

    def reset(self, dashboard_json):
        self._dashboard_json = dashboard_json
        self._dashboard_id = dashboard_json['oid']

    def get_dashboard_id(self):
        return self._dashboard_id

    def get_dashboard_title(self):
        return self._dashboard_json['title']

    def get_dashboard_json(self):
        return self._dashboard_json

    def get_dashboard_folder_id(self):
        return self._dashboard_json['parentFolder']

    def get_dashboard_shares(self):
        """
        Gets the dashboard shares json

        :return: The dashboard shares json
        """

        resp = requests.get(
            '{}/api/shares/dashboard/{}'.format(self._host, self.get_dashboard_id()),
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
            folder_oid = folder.get_folder_oid()
        else:
            folder_oid = None
        resp = requests.patch(
            '{}/api/v1/dashboards/{}'.format(self._host, self.get_dashboard_id()),
            headers=self._token, json={'parentFolder': folder_oid})
        PySenseUtils.parse_response(resp)
        self.reset(resp.json())
        return True


    def share_dashboard_to_user(self, email, rule, subscribe):
        """
        Share a dashboard to a user
        :param email: The email address of the user
        :param rule: The permission of the user on the dashboard (view, edit, etc)
        :param subscribe: true or false, whether to subscribe the user to reports
        :return: The updated share
        """

        user_id = PySenseUtils.get_user_id(self._host, self._token, email)
        shares = self.get_dashboard_shares()
        shares['sharesTo'].append({'shareId': user_id, 'type': 'user', 'rule': rule, 'subscribe': subscribe})
        resp = requests.post(
            '{}/api/shares/dashboard/{}'.format(self._host, self.get_dashboard_id()),
            headers=self._token, json=shares)
        PySenseUtils.parse_response(resp)
        return self.get_dashboard_shares()

    def unshare_dashboard_to_user(self, email):
        """
        Unshare a dashboard to a user
        :param email: The email address of the user
        :return: The updated share
        """

        shares = self.get_dashboard_shares()
        for i, share in enumerate(shares['sharesTo']):
            if share['email'] == email:
                del shares['sharesTo'][i]
        resp = requests.post(
            '{}/api/shares/dashboard/{}'.format(self._host, self.get_dashboard_id()),
            headers=self._token, json=shares)
        PySenseUtils.parse_response(resp)
        return self.get_dashboard_shares()

    def get_dashboard_export_png(self, path, *, include_title=None, include_filters=None, include_ds=None, width=None):
        """
         Get dashboard as png

         :param path: Path to save location of png
         :param include_title: Should dashboard title be included in the exported file
         :param include_filters: Should dashboard filters be included in the exported file
         :param include_ds: Should dashboard data source info be included in the exported file
         :param width: Render width in pixels
         :return: The path of the created file
         """
        param_string = PySenseUtils.build_query_string({
            'includeTitle': include_title,
            'includeFilters': include_filters,
            'includeDs': include_ds,
            'width': width
        })
        resp = requests.get(
            '{}/api/v1/dashboards/{}/export/png?{}'.format(self._host, self.get_dashboard_id(), param_string),
            headers=self._token)
        PySenseUtils.parse_response(resp)
        with open(path, 'wb') as out_file:
            out_file.write(resp.content)
        return path

    def get_dashboard_export_pdf(self, path, paper_format, paper_orientation, layout, *,
                                 include_title=None, include_filters=None, include_ds=None, widget_id=None, preview=None,
                                 row_count=None, show_title=None, show_footer=None, title=None, title_size=None,
                                 title_position=None):
        """
        Get dashboard as pdf

        :param path: Path to save location of pdf
        :param paper_format: What paper format should be used while rendering the dashboard.
        :param paper_orientation: What paper orientation should be used while rendering the dashboard
        :param layout: What layout should be used while rendering the dashboard, as is or feed
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
        :return: The path of the created file
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
                            .format(self._host, self.get_dashboard_id(), param_string), headers=self._token)
        PySenseUtils.parse_response(resp)
        with open(path, 'wb') as out_file:
            out_file.write(resp.content)
        return path

    def get_dashboard_export_dash(self, path):
        """
        Get dashboard as dash file

        :param path: Path to save location of dash file
        :return: The path of the created file
        """
        resp = requests.get('{}/api/v1/dashboards/{}/export/dash'.format(self._host, self.get_dashboard_id()),
                            headers=self._token)
        PySenseUtils.parse_response(resp)
        with open(path, 'wb') as out_file:
            out_file.write(resp.content)
        return path

    def get_dashboard_widgets(self, *, title=None, type=None, subtype=None,
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
        @return: An array of widget objects
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
            '{}/api/v1/dashboards/{}/widgets?{}'.format(self._host, self.get_dashboard_id(), param_string),
            headers=self._token)

        PySenseUtils.parse_response(resp)
        ret_arr = []
        widgets_json = json.loads(resp.content)
        for widget in widgets_json:
            ret_arr.append(PySenseWidget.Widget(self._host, self._token, widget))
        return ret_arr

    def get_dashboards_widget_by_id(self, widget_id, *, fields=None):
        """
        Returns a specific widget (by ID) from a specific dashboard.

        @param widget_id: The ID of the widget to get
        @param fields: Whitelist of fields to return for each document. fields Can also define which fields to exclude
            by prefixing field names with -
        @return: A widget object
        """
        param_string = PySenseUtils.build_query_string({
            'fields': fields
        })

        resp = requests.get('{}/api/v1/dashboards/{}/widgets/{}?{}'.format(self._host, self.get_dashboard_id(),
                                                                           widget_id, param_string),
                            headers=self._token)
        PySenseUtils.parse_response(resp)
        return PySenseWidget.Widget(self._host, self._token, json.loads(resp.content))

    def post_dashboards_widgets(self, widget):
        """
        Adds the provided widget object to the dashboard

        @param widget: widget object to add
        @return: The widget added to the dashboard
        """
        resp = requests.post('{}/api/v1/dashboards/{}/widgets'.format(self._host, self.get_dashboard_id()),
                             headers=self._token, json=widget.get_widget_json())
        PySenseUtils.parse_response(resp)
        return PySenseWidget.Widget(self._host, self._token, json.loads(resp.content))

    def delete_dashboards_widgets(self, widget_id):
        """
        Deletes a widget with the provided ID from it’s dashboard.

        @param widget_id: The ID of the widget to delete
        @return: Response object
        """
        resp = requests.delete('{}/api/v1/dashboards/{}/widgets/{}'
                               .format(self._host, self.get_dashboard_id(), widget_id), headers=self._token)
        return PySenseUtils.parse_response(resp)
