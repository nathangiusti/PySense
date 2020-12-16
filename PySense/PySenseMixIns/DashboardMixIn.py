import json

from PySense import PySenseDashboard, PySenseUtils


class DashboardMixIn:

    def get_dashboards(self, *, parent_folder=None, name=None, data_source_title=None,
                       data_source_address=None, fields=None, sort=None, expand=None):
        """Get all dashboards.

        Args:
            parent_folder (Folder): (Optional) Parent folder to filter by
            name (str): (Optional) Name to filter by
            data_source_title (str): (Optional) Data source name to filter by
            data_source_address (str): (Optional) Data source address to filter by
            fields (list[str]): (Optional) Whitelist of fields to return for each document.
               Can also exclude by prefixing field names with -
            sort (str): (Optional) Field by which the results should be sorted. Ascending by default, descending if prefixed by -
            expand (list[str]): (Optional) List of fields that should be expanded

        Returns:
            list[Dashboard]: A list of the found dashboards
        """

        folder_id = None
        if parent_folder:
            folder_id = parent_folder.get_oid()

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
        """Get all dashboards as an admin

        Args:
            dashboard_type (str): (Optional) Dashboard instance type to filter by. Must be 'owner', 'user', or 'proxy'
            owner_info (bool): (Optional) Whether to return owner_info
            dash_id (str): (Optional) Dashboard ID to filter by
            parent_folder (Folder): (Optional) PySense Folder to filter on
            name (str): (Optional) Name to filter by
            data_source_title (str): (Optional) Data source name to filter by
            data_source_address (str): (Optional) Data source address to filter by
            ownership_type (str): (Optional) Dashboard ownership type to filter by, rewrites “dashboardType” filter.
                Values are: allRoot root owner shared sharedroot ownerAndShared ownerAndSharedByLastOpen
            search (str): (Optional) Search by dashboard title query string or advanced search
            fields (list[str]): (Optional) Whitelist of fields to return for each document.
               Can also exclude by prefixing field names with -
            sort (str): (Optional) Field by which the results should be sorted.
                Ascending by default, descending if prefixed by -
            skip (int): (Optional) Number of results to skip from the start of the data set.
                Skip is to be used with the limit parameter for paging
            limit (int): (Optional) How many results should be returned.
                limit is to be used with the skip parameter for paging
            expand (list[str]): (Optional) List of fields that should be expanded

        Returns:
            list[Dashboard]: An array of all found dashboards
        """

        folder_id = None
        if parent_folder:
            folder_id = parent_folder.get_oid()

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

    def get_dashboard_by_id(self, dashboard_id, *, fields=None, expand=None, admin_access=None):
        """Returns a specific dashboard object by ID.

        Args:
            dashboard_id (str): The ID of the dashboard to get
            fields (list[str]): (Optional) Whitelist of fields to return for each document.
                Fields Can also define which fields to exclude by prefixing field names with -
            expand (list[str]): (Optional) List of fields that should be expanded (substitues their IDs with actual objects).
                May be nested using the resource.subResource format
            admin_access (bool): (Optional) Set to true if logged in as admin and getting unowned dashboard
        Returns:
             Dashboard: Dashboard with the given id.
        """

        query_params = {
            'fields': fields,
            'expand': expand
        }

        if admin_access:
            query_params['adminAccess'] = admin_access
            resp_json = self.connector.rest_call('get', 'api/dashboards/{}'.format(dashboard_id),
                                                 query_params=query_params)
        else:
            resp_json = self.connector.rest_call('get', 'api/v1/dashboards/{}'.format(dashboard_id),
                                                 query_params=query_params)

        return PySenseDashboard.Dashboard(self, resp_json)

    def add_dashboards(self, dashboards):
        """Import given dashboards.

        Args:
            dashboards (list[Dashboard]): Dashboards to import to Sisense

        Returns:
            list[Dashboard]: The new dashboards
        """

        ret_arr = []
        for dashboard in PySenseUtils.make_iterable(dashboards):
            resp = self.connector.rest_call('post', 'api/v1/dashboards', json_payload=dashboard.json)
            ret_arr.append(PySenseDashboard.Dashboard(self, resp))
        return ret_arr

    def delete_dashboards(self, dashboards, *, admin_access=None):
        """Delete dashboards.

        Args:
            dashboards (list[Dashboard]): Dashboards to delete
            admin_access (bool): (Optional) Set to true if logged in as admin and deleting unowned dashboard
        """

        for dashboard in PySenseUtils.make_iterable(dashboards):
            if admin_access is True:
                query_params = {'adminAccess': admin_access}
                self.connector.rest_call('delete', 'api/dashboards/{}'.format(dashboard.get_oid()),
                                         query_params=query_params)
            else:
                self.connector.rest_call('delete', 'api/v1/dashboards/{}'.format(dashboard.get_oid()))

    def create_dashboard(self, title):
        """Create a new default dashboard.

        Args:
            title (str): The title of the dashboard

        Returns:
            Dashboard: The new dashboard
        """

        dashboard_json = json.loads('{"title":"' + title + '","datasource":{"title":"Sample ECommerce","fullname":' \
                         '"LocalHost/Sample ECommerce","id":"aLOCALHOST_aSAMPLEIAAaECOMMERCE","address":"LocalHost",' \
                         '"database":"aSampleIAAaECommerce"},"type":"dashboard","desc":"","filters":[],"style":' \
                         '{"name":"vivid","palette":{"colors":["#00cee6","#9b9bd7","#6EDA55","#fc7570","#fbb755",' \
                         '"#218A8C"],"name":"Vivid","sortOrder":10,"isSystem":true,"systemDefault":true}},' \
                         '"editing":true}')
        resp = self.connector.rest_call('post', 'api/v1/dashboards', json_payload=dashboard_json)
        return PySenseDashboard.Dashboard(self, resp)

    def import_dashboards(self, path, *, action='overwrite', republish=True):
        """Import dashboard file from path

        Can be used to update an existing dashboard.

        Args:
            path (str): The path to the dash file
            action (str): Determines if the dashboard should be overwritten
            republish (bool): Whether to republish after import

        Returns:
            list[Dashboard]: The newly added dashboards
        """

        query_params = {'action': action, 'republish': republish}
        json_obj = PySenseUtils.read_json(path)

        if isinstance(json_obj, list):
            json_array = json_obj
        else:
            json_array = [json_obj]

        result_json = self.connector.rest_call('post', 'api/v1/dashboards/import/bulk',
                                               query_params=query_params, json_payload=json_array)
        ret_arr = []
        for dashboard_json in result_json["succeded"]:
            ret_arr.append(PySenseDashboard.Dashboard(self, dashboard_json))
        return ret_arr

    def export_dashboards(self, dashboards, path, *, admin_access=None):
        """Get dashboard as dash file.

        Args:
            dashboards (list[Dashboard]): One to many dashboards to back up to dash file
            path (str): Path to save location of dash file
            admin_access (bool): (Optional) Set to true if logged in as admin and exporting unowned dashboard
        Returns:
            str: The path of the created file
        """

        query_params = {'dashboardIds': [], 'adminAccess': admin_access}
        for dashboard in PySenseUtils.make_iterable(dashboards):
            query_params['dashboardIds'].append(dashboard.get_oid())

        self.connector.rest_call('get', 'api/v1/dashboards/export', path=path, query_params=query_params)

        return path

