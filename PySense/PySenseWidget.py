class Widget:

    def __init__(self, py_client, widget_json):
        self._py_client = py_client
        self._widget_json = widget_json

    def get_json(self):
        """Returns the widget's JSON."""
        return self._widget_json

    def get_dashboard_id(self):
        """Returns the dashboard id of the widget."""
        return self._widget_json['dashboardid']

    def get_oid(self):
        """Gets the widget's id"""
        return self._widget_json['oid']

    def export_to_png(self, width, height, *, path=None):
        """Export's widget to png.

        Args:
            width: Render width in pixels
            height: Render height in pixels
            path: (optional) Path to save the file

        Returns:
            The path of the saved file if set, else the raw content
        """
        query_params = {'width': width, 'height': height}
        resp_content = self._py_client.connector.rest_call('get', 'api/v1/dashboards/{}/widgets/{}/export/png'
                                                           .format(self.get_dashboard_id(), self.get_oid()),
                                                           query_params=query_params, raw=True)
        if path is not None:
            with open(path, 'wb') as out_file:
                out_file.write(resp_content)
            return path
        else:
            return resp_content
