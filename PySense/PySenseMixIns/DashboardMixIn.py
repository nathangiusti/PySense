import json

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

    def get_dashboards_admin(self, *, dashboard_type=None, owner_info=None, dash_id=None, parent_folder=None, name=None,
                             data_source_title=None, data_source_address=None, ownership_type=None, search=None,
                             fields=None, sort=None, skip=None, limit=None, expand=None):
        """Get all dashboards.

        Args:
            dashboard_type: (Optional) Dashboard instance type to filter by. Must be 'owner', 'user', or 'proxy'
            owner_info: (Optional) Dashboard owner information. True or False
            dash_id: (optional) Dashboard ID to filter by
            parent_folder: (Optional) PySense Folder to filter on
            name: (Optional) Name to filter by
            data_source_title: (Optional) Data source name to filter by
            data_source_address: (Optional) Data source address to filter by
            ownership_type: (Optional) Dashboard ownership type to filter by, rewrites “dashboardType” filter.
            Values are: allRoot root owner shared sharedroot ownerAndShared ownerAndSharedByLastOpen
            search: (Optional) Search by dashboard title query string or advanced search
            fields: (Optional) Whitelist of fields to return for each document.
               Can also exclude by prefixing field names with -
            sort: (optional) Field by which the results should be sorted.
                Ascending by default, descending if prefixed by -
            skip: (optional) Number of results to skip from the start of the data set.
                Skip is to be used with the limit parameter for paging
            limit: (optional) How many results should be returned.
                limit is to be used with the skip parameter for paging
            expand: (Optional) List of fields that should be expanded

        Returns:
            An array of all found dashboards
        """

        folder_id = None
        if parent_folder:
            folder_id = parent_folder.get_id()

        query_params = {
            'dashboardType': dashboard_type,
            'ownerInfo': owner_info,
            'id': dash_id,
            'parentFolder': folder_id,
            'name': name,
            'datasourceTitle': data_source_title,
            'datasourceAddress': data_source_address,
            'ownershipType': ownership_type,
            'fields': fields,
            'search': search,
            'sort': sort,
            'skip': skip,
            'limit': limit,
            'expand': expand
        }
        json_arr = self.connector.rest_call('get', 'api/v1/dashboards/admin', query_params=query_params)

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

    def create_dashboard(self, title):
        """Create a new dashboard.

        Args:
            title: The title of the dashboard

        Returns:
            The new dashboard
        """

        dashboard_json = json.loads('{"title":"' + title + '","datasource":{"title":"Sample ECommerce","fullname":' \
                         '"LocalHost/Sample ECommerce","id":"aLOCALHOST_aSAMPLEIAAaECOMMERCE","address":"LocalHost",' \
                         '"database":"aSampleIAAaECommerce"},"type":"dashboard","desc":"","filters":[],"style":' \
                         '{"name":"vivid","palette":{"colors":["#00cee6","#9b9bd7","#6EDA55","#fc7570","#fbb755",' \
                         '"#218A8C"],"name":"Vivid","sortOrder":10,"isSystem":true,"systemDefault":true}},' \
                         '"editing":true}')
        resp = self.connector.rest_call('post', 'api/v1/dashboards', json_payload=dashboard_json)
        return PySenseDashboard.Dashboard(self, resp)
