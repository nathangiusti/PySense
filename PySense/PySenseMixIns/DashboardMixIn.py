from PySense import PySenseDashboard
from PySense import PySenseUtils


class DashboardMixIn:

    def get_dashboards(self, *, parent_folder=None, name=None, data_source_title=None,
                       data_source_address=None, fields=None, sort=None, expand=None):
        """Get all dashboards.

        Args:
            parent_folder: Parent folder to filter by
            name: Name to filter by
            data_source_title: Data source name to filter by
            data_source_address: Data source address to filter by
            fields: Whitelist of fields to return for each document.
               Can also exclude by prefixing field names with -
            sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -
            expand: List of fields that should be expanded

        Returns:
            An array of all found dashboards
        """

        folder_id = None
        if parent_folder:
            folder_id = parent_folder.get_id()

        query_params = {
            'parentFolder': folder_id,
            'name': name,
            'datasourceTitle': data_source_title,
            'datasourceAddress': data_source_address,
            'fields': fields,
            'sort': sort,
            'expand': expand
        }
        json_arr = self.connector.rest_call('get', 'api/v1/dashboards', query_params=query_params)

        ret_arr = []
        for dash in json_arr:
            ret_arr.append(PySenseDashboard.Dashboard(self, dash))
        return ret_arr

    def get_dashboard_by_id(self, dashboard_id, *, fields=None, expand=None):
        """Returns a specific dashboard object by ID.

        Args:
            dashboard_id: The ID of the dashboard to get
            fields: (optional) Whitelist of fields to return for each document.
                Fields Can also define which fields to exclude by prefixing field names with -
            expand: (optional) List of fields that should be expanded (substitues their IDs with actual objects).
                May be nested using the resource.subResource format

        Returns:
             Dashboard with the given id.
        """

        query_params = {
            'fields': fields,
            'expand': expand
        }

        resp_json = self.connector.rest_call('get', 'api/v1/dashboards/{}'.format(dashboard_id),
                                             query_params=query_params)

        return PySenseDashboard.Dashboard(self, resp_json)

    def add_dashboards(self, dashboards):
        """Import given dashboards.

        Args:
            dashboards: One to many PySense dashboard to import

        Returns:
            An array of new dashboards
        """
        ret_arr = []
        for dashboard in PySenseUtils.make_iterable(dashboards):
            resp = self.connector.rest_call('post', 'api/v1/dashboards', json_payload=dashboard.get_json())
            ret_arr.append(PySenseDashboard.Dashboard(self, resp))
        return ret_arr

    def delete_dashboards(self, dashboards):
        """Delete dashboards.

        Args:
            dashboards: Dashboards to delete
        """
        for dashboard in PySenseUtils.make_iterable(dashboards):
            self.connector.rest_call('delete', 'api/v1/dashboards/{}'.format(dashboard.get_id()))
