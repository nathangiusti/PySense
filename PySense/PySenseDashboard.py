from PySense import PySenseGroup
from PySense import PySenseException
from PySense import PySenseUser
from PySense import PySenseUtils
from PySense import PySenseWidget


class Dashboard:

    def __init__(self, py_client, dashboard_json):
        self._dashboard_json = dashboard_json
        self._py_client = py_client

    def _reset(self):
        self._dashboard_json = self._py_client.connector.rest_call('get', 'api/v1/dashboards/{}'.format(self.get_id()))

    def get_json(self):
        """Returns dashboard json"""
        return self._dashboard_json

    def get_datasource(self):
        """Returns the elasticube powering the dashboard.

        Not reliable when multiple elasticubes on dashboard.
        """
        if 'datasource' in self._dashboard_json:
            return self._py_client.get_elasticube_by_name(self._dashboard_json['datasource']['title'])
        else:
            None

    def get_id(self):
        """Gets the dashboard's id"""
        return self._dashboard_json['oid']

    def get_title(self):
        """Gets the dashboard's title"""
        if 'title' in self._dashboard_json:
            return self._dashboard_json['title']
        else:
            return None

    def get_folder(self):
        """Gets the dashboards folder"""
        if 'parentFolder' in self._dashboard_json:
            return self._py_client.get_folder_by_id(self._dashboard_json['parentFolder'])
        else:
            return None

    def get_shares(self, *, admin_access=None):
        """Gets the dashboard shares json

        Args:
            admin_access: (Optional) Set to true if logged in as admin and getting unowned dashboard
        """

        query_params = {
            'adminAccess': admin_access
        }

        try:
            resp_json = self._py_client.connector.rest_call('get', 'api/shares/dashboard/{}'.format(self.get_id()),
                                                            query_params=query_params)
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
        except PySenseException.PySenseException:
            return self._dashboard_json['shares']

    def get_share_users_groups(self, *, admin_access=None):
        """Gets a list of users and groups the dashboard is shared with

        Args:
            admin_access: (Optional) Set to true if logged in as admin and getting unowned dashboard
        """

        query_params = {
            'adminAccess': admin_access
        }

        resp_json = self._py_client.connector.rest_call('get', 'api/shares/dashboard/{}'.format(self.get_id()),
                                                        query_params=query_params)
        ret_arr = []
        for share in resp_json['sharesTo']:
            if share['type'] == 'user':
                ret_arr.append(self._py_client.get_user_by_id(share['shareId']))
            elif share['type'] == 'group':
                ret_arr.append(self._py_client.get_group_by_id(share['shareId']))
        return ret_arr

    def add_share(self, shares, rule, subscribe, *, share_cube=True, admin_access=None):
        """Share a dashboard to a new group or user.

        If dashboard is already shared with user or group, nothing happens

        By default gives query permission to the cube as well. Set share_cubes to false to not update cube shares

        Args:
            shares: One to many PySense Groups or Users
            rule: The permission of the user on the dashboard (view, edit, etc)
            subscribe: true or false, whether to subscribe the user to reports
            share_cube: (Optional) False to not share cube with groups/users
            admin_access: (Optional) Set to true if logged in as admin and getting unowned dashboard
        """

        query_params = {
            'adminAccess': admin_access
        }

        curr_shares = self.get_shares(admin_access=admin_access)

        for share in shares:
            share_id = share.get_id()
            for curr_share in curr_shares['sharesTo']:
                if 'shareId' == curr_share['shareId']:
                    share_id = None

            if share_id is not None:
                if isinstance(share, PySenseUser.User):
                    curr_shares['sharesTo'].append(
                        {'shareId': share.get_id(), 'type': 'user', 'rule': rule, 'subscribe': subscribe}
                    )
                elif isinstance(share, PySenseGroup.Group):
                    curr_shares['sharesTo'].append(
                        {'shareId': share.get_id(), 'type': 'group', 'rule': rule, 'subscribe': subscribe}
                    )

        self._py_client.connector.rest_call('post', 'api/shares/dashboard/{}'.format(self.get_id()),
                                            json_payload=curr_shares, query_params=query_params)
        if share_cube:
            data_source = self.get_datasource()
            data_source.add_share(shares)

    def remove_shares(self, shares, *, admin_access=None):
        """Unshare a dashboard to a list of groups and users

        Args:
            shares: Groups and users to unshare the dashboard with
            admin_access: (Optional) Set to true if logged in as admin and getting unowned dashboard
        """

        query_params = {
            'adminAccess': admin_access
        }

        share_ids_to_delete = []
        for shares in PySenseUtils.make_iterable(shares):
            share_ids_to_delete.append(shares.get_id())
        current_shares = self.get_shares(admin_access=admin_access)
        for share_id in share_ids_to_delete:
            for i, shares in enumerate(current_shares['sharesTo']):
                if shares['shareId'] == share_id:
                    del current_shares['sharesTo'][i]
        self._py_client.connector.rest_call('post', 'api/shares/dashboard/{}'.format(self.get_id()),
                                            json_payload=current_shares, query_params=query_params)

    def move_to_folder(self, folder):
        """Move dashboard to given folder"""
        if folder:
            folder_oid = folder.get_oid()
        else:
            folder_oid = None
        self._py_client.connector.rest_call('patch', 'api/v1/dashboards/{}'.format(self.get_id()),
                                            json_payload={'parentFolder': folder_oid})
        self._reset()

    def export_to_png(self, *, path=None, include_title=None, include_filters=None, include_ds=None, width=None):
        """Get dashboard as png

        Args:
            path: (optional) Path to save location of png
            include_title: (optional) Should dashboard title be included in the exported file
            include_filters: (optional) Should dashboard filters be included in the exported file
            include_ds: (optional) Should dashboard data source info be included in the exported file
            width: (optional) Render width in pixels

        Returns:
            The path of the created file if provided or else the raw response object
        """

        query_params = {
            'includeTitle': include_title,
            'includeFilters': include_filters,
            'includeDs': include_ds,
            'width': width
        }
        resp_content = self._py_client.connector.rest_call('get', 'api/v1/dashboards/{}/export/png'
                                                           .format(self.get_id()), query_params=query_params, raw=True)
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
        """Get dashboard as pdf

        Args:
            paper_format: What paper format should be used while rendering the dashboard.
            paper_orientation: What paper orientation should be used while rendering the dashboard
            layout: What layout should be used while rendering the dashboard, as is or feed
            path: (optional) Path to save location of pdf
            include_title: (optional) Should dashboard title be included in the exported file
            include_filters: (optional) Should dashboard filters be included in the exported file
            include_ds: (optional) Should dashboard datasource info be included in the exported file
            widget_id: (optional) Widget Id (Use only for Table and Pivot Widgets)
            preview: (optional) Should use a new Pixel Perfect Reporting
            row_count: (optional) Count of Table/Pivot rows to export
            show_title: (optional) Should Table/Pivot Widget title be included in the exported file
            show_footer: (optional) Should Table/Pivot Widget footer be included in the exported file
            title: (optional) Table/Pivot Widget title text in the exported file
            title_size: (optional) Table/Pivot widget title size in the exported file
            title_position: (optional) Table/Pivot widget title position in the exported file

        Returns:
             The path of the created file if provided, else the raw content
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
        resp_content = self._py_client.connector.rest_call('get', 'api/v1/dashboards/{}/export/pdf'
                                                           .format(self.get_id()), query_params=query_params)

        if path is not None:
            with open(path, 'wb') as out_file:
                out_file.write(resp_content)
            return path
        else:
            return resp_content

    def export_to_dash(self, *, path=None, admin_access=None):
        """Get dashboard as dash file.

        Args:
            path: (optional) Path to save location of dash file
            admin_access: (Optional) Set to true if logged in as admin and getting unowned dashboard
        Returns:
            The path of the created file if path provided, else the raw content
        """

        if admin_access:
            query_params = {'adminAccess': admin_access}
            resp_content = self._py_client.connector.rest_call('get', 'api/dashboards/{}/export'
                                                               .format(self.get_id()), raw=True,
                                                               query_params=query_params)
        else:
            resp_content = self._py_client.connector.rest_call('get', 'api/v1/dashboards/{}/export/dash'
                                                               .format(self.get_id()), raw=True)
        if path is not None:
            with open(path, 'wb') as out_file:
                out_file.write(resp_content)
            return path
        else:
            return resp_content

    def get_widgets(self, *, title=None, type=None, subtype=None,
                    fields=None, sort=None, skip=None, limit=None, id=None):
        """Returns an array of a dashboard’s widgets.

        Args:
            title: (optional) Widget title to filter by
            type: (optional) Widget type to filter by
            subtype: (optional) Widget sub-type to filter by
            fields: (optional) Whitelist of fields to return for each document. fields Can also define which fields to exclude
                by prefixing field names with -
            sort: (optional) Field by which the results should be sorted. Ascending by default, descending if prefixed by -
            skip: (optional) Number of results to skip from the start of the data set. skip is to be used with the limit
                parameter for paging
            limit: (optional) How many results should be returned. limit is to be used with the skip parameter for paging
            id: (Optional) If set, will return only the widget with matching id or all widgets if that id is not found

        Returns:
            An array of widget objects
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
        resp_json = self._py_client.connector.rest_call('get', 'api/v1/dashboards/{}/widgets'.format(self.get_id()),
                                              query_params=query_params)
        for widget in resp_json:
            dash_widget = PySenseWidget.Widget(self._py_client, widget)
            if id is not None and dash_widget.get_oid() == id:
                return dash_widget
            ret_arr.append(dash_widget)
        return ret_arr

    def get_widget_by_id(self, widget_id, *, fields=None):
        """Returns a specific widget (by ID) from a specific dashboard.

        Args:
            widget_id: The ID of the widget to get
            fields: (optional) Whitelist of fields to return for each document.
                Fields Can also define which fields to exclude by prefixing field names with -

        Returns:
            A widget object
        """

        query_params = {
            'fields': fields
        }

        resp_json = self._py_client.connector.rest_call('get', 'api/v1/dashboards/{}/widgets/{}'
                                                        .format(self.get_id(), widget_id), query_params=query_params)
        return PySenseWidget.Widget(self._py_client, resp_json)

    def add_widget(self, widget):
        """Adds the provided widget object to the dashboard.

        Args:
            widget: PySenseWidget.Widget object to add

        Returns:
            The widget added to the dashboard
        """

        resp_json = self._py_client.connector.rest_call('post', 'api/v1/dashboards/{}/widgets'.format(self.get_id()),
                                                        json_payload=widget.get_json())
        return PySenseWidget.Widget(self._py_client, resp_json)

    def delete_widget(self, widgets):
        """Deletes widgets from it’s dashboard."""
        for widget in PySenseUtils.make_iterable(widgets):
            self._py_client.connector.rest_call('delete', 'api/v1/dashboards/{}/widgets/{}'
                                                .format(self.get_id(), widget.get_oid()))
        self._reset()

    def remove_ghost_widgets(self):
        """Removes ghost widgets from dashboard"""
        patch_json = {"layout": self._dashboard_json['layout']}
        modified = True
        while modified:
            modified = False
            for n, column in enumerate(patch_json['layout']['columns']):
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
                    patch_json['layout']['columns'].pop(n)
        self._py_client.connector.rest_call('patch', 'api/v1/dashboards/{}'.format(self.get_id()),
                                            json_payload=patch_json)
        self._reset()

    def does_widget_exist(self, widget_id):
        """Returns true or false if the widget with id is in the dashboard"""
        try:
            self.get_widget_by_id(widget_id)
        except PySenseException.PySenseException:
            return False
        else:
            return True

    def get_owner(self):
        """Returns the user object that owns this dashboard"""
        return self._py_client.get_user_by_id(self._dashboard_json['owner'])

    def get_last_updated(self):
        """Returns the last updated time for the dashboard"""
        if 'lastUpdated' in self._dashboard_json:
            return PySenseUtils.sisense_time_to_python(self._dashboard_json['lastUpdated'])
        else:
            return None

    def get_last_opened(self):
        """Returns the last updated time for the dashboard"""
        if 'lastOpened' in self._dashboard_json:
            return PySenseUtils.sisense_time_to_python(self._dashboard_json['lastOpened'])
        else:
            return None

    def publish(self):
        """Publishes the dashboard"""
        self._py_client.connector.rest_call('post', 'api/v1/dashboards/{}/publish'.format(self.get_id()))

    def get_created_date(self):
        """Returns the creation datetime of the dashboard"""
        return PySenseUtils.sisense_time_to_python(self._dashboard_json['created'])
