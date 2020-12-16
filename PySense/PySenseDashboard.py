from PySense import PySenseGroup, PySenseException, PySenseUser, PySenseUtils, PySenseWidget


class Dashboard:
    """A Sisense Dashboard

    Attributes:
        json (JSON): The JSON for this object
        py_client (PySense): The connection to the Sisense server which owns this asset
    """

    def __init__(self, py_client, json):
        """

        Args:
            py_client (PySense): The PySense object for the server this asset belongs to
            json (JSON): The json for this object
        """

        self.json = json
        self.py_client = py_client

    def _reset(self):
        self.json = self.py_client.connector.rest_call('get', 'api/v1/dashboards/{}'.format(self.get_oid()))

    def get_datasource(self):
        """Returns the elasticube powering the dashboard.

        Not reliable when multiple elasticubes on dashboard.
        """

        if 'datasource' in self.json:
            return self.py_client.get_elasticube_by_name(self.json['datasource']['title'])
        else:
            None

    def get_oid(self):
        """Gets the dashboard's oid"""

        return self.json['oid']

    def get_title(self):
        """Gets the dashboard's title"""

        if 'title' in self.json:
            return self.json['title']
        else:
            return None

    def get_folder(self):
        """Gets the dashboards folder"""

        if 'parentFolder' in self.json:
            return self.py_client.get_folder_by_id(self.json['parentFolder'])
        else:
            return None

    def get_shares_json(self, *, admin_access=None):
        """Gets the dashboard shares json

        Args:
            admin_access (bool): (Optional) Set to true if logged in as admin and getting unowned dashboard

        Returns:
            JSON: A shares JSON blob
        """

        query_params = {
            'adminAccess': admin_access
        }

        try:
            resp_json = self.py_client.connector.rest_call('get', 'api/shares/dashboard/{}'.format(self.get_oid()),
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
            return self.json['shares']

    def get_share_users_groups(self, *, admin_access=None):
        """Gets a list of users and groups the dashboard is shared with

        Args:
            admin_access (bool): (Optional) Set to true if logged in as admin and getting unowned dashboard

        Returns:
            list[User,Group]: A list of users and groups the dashboard is shared with
        """

        query_params = {
            'adminAccess': admin_access
        }

        resp_json = self.py_client.connector.rest_call('get', 'api/shares/dashboard/{}'.format(self.get_oid()),
                                                       query_params=query_params)
        ret_arr = []
        for share in resp_json['sharesTo']:
            if share['type'] == 'user':
                ret_arr.append(self.py_client.get_user_by_id(share['shareId']))
            elif share['type'] == 'group':
                ret_arr.append(self.py_client.get_group_by_id(share['shareId']))
        return ret_arr

    def add_share(self, shares, rule, subscribe, *, share_cube=True, admin_access=None):
        """Share a dashboard to a new group or user.

        If dashboard is already shared with user or group, nothing happens

        By default gives query permission to the cube as well. Set share_cubes to false to not update cube shares

        Args:
            shares (list[Group,User]): One to many PySense Groups or Users
            rule (str): The permission of the user on the dashboard (view, edit, etc)
            subscribe (bool): Whether to subscribe the user to reports
            share_cube (bool): (Optional) If set to false user will not get dashboard results.
            admin_access (bool): (Optional) Set to true if logged in as admin and getting unowned dashboard
        """

        query_params = {
            'adminAccess': admin_access
        }

        curr_shares = self.get_shares_json(admin_access=admin_access)

        for share in PySenseUtils.make_iterable(shares):
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

        self.py_client.connector.rest_call('post', 'api/shares/dashboard/{}'.format(self.get_oid()),
                                           json_payload=curr_shares, query_params=query_params)
        if share_cube:
            data_source = self.get_datasource()
            data_source.add_share(shares)

    def remove_shares(self, shares, *, admin_access=None):
        """Unshare a dashboard to a list of groups and users

        Args:
            shares (list[Group,User]): Groups and users to unshare the dashboard with
            admin_access (bool): (Optional) Set to true if logged in as admin and getting unowned dashboard
        """

        query_params = {
            'adminAccess': admin_access
        }

        share_ids_to_delete = []
        for shares in PySenseUtils.make_iterable(shares):
            share_ids_to_delete.append(shares.get_id())
        current_shares = self.get_shares_json(admin_access=admin_access)
        for share_id in share_ids_to_delete:
            for i, shares in enumerate(current_shares['sharesTo']):
                if shares['shareId'] == share_id:
                    del current_shares['sharesTo'][i]
        self.py_client.connector.rest_call('post', 'api/shares/dashboard/{}'.format(self.get_oid()),
                                           json_payload=current_shares, query_params=query_params)

    def move_to_folder(self, folder):
        """Move dashboard to given folder

        Args:
            folder (Folder): The folder object to move the dashboard into
        """

        folder_oid = folder.get_oid()

        self.py_client.connector.rest_call('patch', 'api/v1/dashboards/{}'.format(self.get_oid()),
                                           json_payload={'parentFolder': folder_oid})
        self._reset()

    def export_to_png(self, path, *, include_title=None, include_filters=None, include_ds=None, width=None):
        """Get dashboard as png

        Args:
            path (str): Path to save location of png
            include_title (bool): (Optional) Should dashboard title be included in the exported file
            include_filters (bool): (Optional) Should dashboard filters be included in the exported file
            include_ds (bool): (Optional) Should dashboard data source info be included in the exported file
            width (int): (Optional) Render width in pixels

        Returns:
            str: The path of the created file
        """

        query_params = {
            'includeTitle': include_title,
            'includeFilters': include_filters,
            'includeDs': include_ds,
            'width': width
        }
        self.py_client.connector.rest_call('get', 'api/v1/dashboards/{}/export/png'.format(self.get_oid()),
                                           query_params=query_params, path=path, raw=True)

        return path

    def export_to_pdf(self, paper_format, paper_orientation, layout, path, *,
                      include_title=None, include_filters=None, include_ds=None, widget_id=None,
                      preview=None,
                      row_count=None, show_title=None, show_footer=None, title=None, title_size=None,
                      title_position=None):
        """Get dashboard as pdf

        Args:
            paper_format (str): What paper format should be used while rendering the dashboard.
            paper_orientation (str): What paper orientation should be used while rendering the dashboard
            layout (str): What layout should be used while rendering the dashboard, as is or feed
            path (str): Path to save location of pdf
            include_title (bool): (Optional) Should dashboard title be included in the exported file
            include_filters (bool): (Optional) Should dashboard filters be included in the exported file
            include_ds (bool): (Optional) Should dashboard datasource info be included in the exported file
            widget_id (str): (Optional) Widget Id (Use only for Table and Pivot Widgets)
            preview (bool): (Optional) Should use a new Pixel Perfect Reporting
            row_count (int): (Optional) Count of Table/Pivot rows to export
            show_title (bool): (Optional) Should Table/Pivot Widget title be included in the exported file
            show_footer (bool): (Optional) Should Table/Pivot Widget footer be included in the exported file
            title (str): (Optional) Table/Pivot Widget title text in the exported file
            title_size (int): (Optional) Table/Pivot widget title size in the exported file
            title_position (str): (Optional) Table/Pivot widget title position in the exported file

        Returns:
             str: The path of the created file
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
        self.py_client.connector.rest_call('get', 'api/v1/dashboards/{}/export/pdf'.format(self.get_oid()),
                                           query_params=query_params, path=path, raw=True)

        return path

    def export_to_dash(self, path, *, admin_access=None):
        """Get dashboard as dash file.

        Args:
            path (str): Path to save location of dash file
            admin_access (bool): (Optional) Set to true if logged in as admin and getting unowned dashboard
        Returns:
            str: The path of the created file if path provided
        """

        query_params = {
            'dashboardIds': [self.get_oid()],
            'adminAccess': admin_access
        }

        self.py_client.connector.rest_call('get', 'api/v1/dashboards/export', path=path, query_params=query_params)

        return path

    def get_widgets(self, *, title=None, type=None, subtype=None,
                    fields=None, sort=None, skip=None, limit=None, widget_id=None):
        """Returns an array of a dashboard’s widgets.

        Args:
            title (str): (Optional) Widget title to filter by
            type (str): (Optional) Widget type to filter by
            subtype (str): (Optional) Widget sub-type to filter by
            fields (str): (Optional) Whitelist of fields to return for each document. fields Can also define which fields to exclude
                by prefixing field names with -
            sort (str): (Optional) Field by which the results should be sorted. Ascending by default, descending if prefixed by -
            skip (int): (Optional) Number of results to skip from the start of the data set. skip is to be used with the limit
                parameter for paging
            limit (int): (Optional) How many results should be returned. limit is to be used with the skip parameter for paging
            widget_id (str): (Optional) If set, will return only the widget with matching id or all widgets if that id is not found

        Returns:
            list[Widget]: A list of widgets
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
        resp_json = self.py_client.connector.rest_call('get', 'api/v1/dashboards/{}/widgets'.format(self.get_oid()),
                                                       query_params=query_params)
        for widget in resp_json:
            dash_widget = PySenseWidget.Widget(self.py_client, widget)
            if widget_id is not None and dash_widget.get_oid() == widget_id:
                return dash_widget
            ret_arr.append(dash_widget)
        return ret_arr

    def get_widget_by_id(self, widget_id, *, fields=None):
        """Returns a specific widget (by ID) from a specific dashboard.

        Args:
            widget_id (str): The ID of the widget to get
            fields (list[str]): (Optional) Whitelist of fields to return for each document.
                Fields Can also define which fields to exclude by prefixing field names with -

        Returns:
            Widget: A widget object
        """

        query_params = {
            'fields': fields
        }

        resp_json = self.py_client.connector.rest_call('get', 'api/v1/dashboards/{}/widgets/{}'
                                                       .format(self.get_oid(), widget_id), query_params=query_params)
        return PySenseWidget.Widget(self.py_client, resp_json)

    def add_widget(self, widget):
        """Adds the provided widget object to the dashboard.

        Args:
            widget (Widget): Widget object to add

        Returns:
            Widget: The widget added to the dashboard
        """

        resp_json = self.py_client.connector.rest_call('post', 'api/v1/dashboards/{}/widgets'.format(self.get_oid()),
                                                       json_payload=widget.get_json())
        return PySenseWidget.Widget(self.py_client, resp_json)

    def delete_widget(self, widgets):
        """Deletes widgets from its dashboard.

        Args:
            widgets (list[Widget]): Widgets to delete
        """

        for widget in PySenseUtils.make_iterable(widgets):
            self.py_client.connector.rest_call('delete', 'api/v1/dashboards/{}/widgets/{}'
                                               .format(self.get_oid(), widget.get_oid()))
        self._reset()

    def remove_ghost_widgets(self):
        """Removes ghost widgets from dashboard"""

        patch_json = {"layout": self.json['layout']}
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
        self.py_client.connector.rest_call('patch', 'api/v1/dashboards/{}'.format(self.get_oid()),
                                           json_payload=patch_json)
        self._reset()

    def does_widget_exist(self, widget_id):
        """Checks if a widget exists in dashboard

        Args:
            widget_id (str): The widget id to look for

        Returns:
            bool: Whether the widget is in the dashboard
        """

        try:
            self.get_widget_by_id(widget_id)
        except PySenseException.PySenseException:
            return False
        else:
            return True

    def get_owner(self):
        """Returns the user object that owns this dashboard

        Returns:
            User: The PySense User who owns this dashboard
        """

        return self.py_client.get_user_by_id(self.json['owner'])

    def get_last_updated(self):
        """Returns the last updated time for the dashboard

        Returns:
            datetime: The last updated datetime
        """

        if 'lastUpdated' in self.json:
            return PySenseUtils.sisense_time_to_python(self.json['lastUpdated'])
        else:
            return None

    def get_last_opened(self):
        """Returns the last opened time for the dashboard

        Returns:
            datetime: The last opened datetime
        """

        if 'lastOpened' in self.json:
            return PySenseUtils.sisense_time_to_python(self.json['lastOpened'])
        else:
            return None

    def publish(self):
        """Publishes the dashboard"""

        self.py_client.connector.rest_call('post', 'api/v1/dashboards/{}/publish'.format(self.get_oid()))

    def get_created_date(self):
        """Returns the creation datetime of the dashboard

        Returns:
            datetime: The created datetime
        """
        return PySenseUtils.sisense_time_to_python(self.json['created'])

    def remap_field(self, old_table, old_column, new_table, new_column):
        """Remaps all widgets and filters from the old table.old column to new table.new column

        Does not work with date fields

        Args:
            old_table (str): The old table name
            old_column (str): The old column name
            new_table (str): The new table name
            new_column (str): The new column name
        """

        for widget in self.get_widgets():
            widget.remap_field(old_table, old_column, new_table, new_column)
        filters = self.json['filters']
        for f in filters:
            PySenseUtils.update_jaql(old_table, old_column, new_table, new_column, f['jaql'])
        payload = {"filters": filters}
        self.py_client.connector.rest_call('patch', 'api/v1/dashboards/{}'.format(self.get_oid()),
                                           json_payload=payload)

    def change_owner(self, new_owner, *, can_edit=True, admin_access=None):
        """Change the owner of the dashboard to new_owner

        Args:
            new_owner (User): The PySense User to transfer ownership to
            can_edit (bool): (Optional) Set to false to allow original owner viewer rights only
            admin_access (bool): (Optional) Set to true if logged in as admin and using unowned dashboard
        """

        json_payload = {
            "ownerId": new_owner.get_id(),
            "originalOwnerRule": "edit" if can_edit else "view"
        }
        self.py_client.connector.rest_call('post', 'api/v1/dashboards/{}/change_owner'.format(self.get_oid()),
                                           json_payload=json_payload, query_params={'adminAccess': admin_access})
