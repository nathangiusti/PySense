from PySense import PySenseUtils


class Widget:
    """A widget on a dashboard

    A widget belongs to one dashboard.

    Attributes:
        json (JSON): The JSON for this object
        py_client (PySense): The connection to the Sisense server which owns this asset
    """

    def __init__(self, py_client, widget_json):
        """

        Args:
            py_client (PySense): The PySense object for the server this asset belongs to
            widget_json (JSON): The json for this object
        """

        self.py_client = py_client
        self.json = widget_json

    def get_json(self):
        """Returns the widget's JSON."""

        return self.json

    def get_dashboard_id(self):
        """Returns the dashboard id of the widget."""
        return self.json['dashboardid']

    def get_oid(self):
        """Gets the widget's id"""
        return self.json['oid']

    def export_to_png(self, width, height, path):
        """Export's widget to png.

        Args:
            width: Render width in pixels
            height: Render height in pixels
            path: Path to save the file

        Returns:
            str: The path of the saved file
        """
        query_params = {'width': width, 'height': height}
        self.py_client.connector.rest_call('get', 'api/v1/dashboards/{}/widgets/{}/export/png'
                                           .format(self.get_dashboard_id(), self.get_oid()),
                                           query_params=query_params, path=path, raw=True)
        return path

    def remap_field(self, old_table, old_column, new_table, new_column):
        """Remaps all usages of old_table and old_column in a widget to new_table and new_column respectively

        Args:
            old_table: The old table name
            old_column: The old column name
            new_table: The new table name
            new_column: The new column name
        """
        panels = self.json["metadata"]["panels"]
        for panel in panels:
            items = panel["items"]
            if panel["name"] == "rows":
                for item in items:
                    if "jaql" in item:
                        PySenseUtils.update_jaql(old_table, old_column, new_table, new_column,  item["jaql"])
                    if "field" in item and "id" in item["field"]:
                        item["field"]["id"] = "[{}.{}]".format(new_table, new_column)
            if panel["name"] == "values":
                for item in items:
                    if "jaql" in item and "context" in item["jaql"]:
                        for context in item["jaql"]["context"]:
                            PySenseUtils.update_jaql(old_table, old_column, new_table, new_column,
                                                     item["jaql"]["context"][context])
            if panel["name"] in ["columns", "filters"]:
                for item in items:
                    if "jaql" in item:
                        PySenseUtils.update_jaql(old_table, old_column, new_table, new_column, item["jaql"])

        update_json = {"metadata": self.json["metadata"]}
        self.py_client.connector.rest_call('patch', 'api/v1/dashboards/{}/widgets/{}'
                                           .format(self.get_dashboard_id(), self.get_oid()), json_payload=update_json)



