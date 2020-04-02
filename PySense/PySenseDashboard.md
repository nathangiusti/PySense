Module PySense.PySenseDashboard
===============================

Classes
-------

`Dashboard(host, token, dashboard_json)`
:   

    ### Methods

    `delete_dashboards_widgets(self, widget_id)`
    :   Deletes a widget with the provided ID from it’s dashboard.
        
        @param widget_id: The ID of the widget to delete
        @return: True

    `does_widget_exist(self, widget_id)`
    :   Returns whether or not a widget with the given id is in the dashboard
        :param widget_id: The widget id to look for
        :return: True if found, false if not.

    `get_dashboard_export_dash(self, path)`
    :   Get dashboard as dash file
        
        :param path: Path to save location of dash file
        :return: The path of the created file

    `get_dashboard_export_pdf(self, path, paper_format, paper_orientation, layout, *, include_title=None, include_filters=None, include_ds=None, widget_id=None, preview=None, row_count=None, show_title=None, show_footer=None, title=None, title_size=None, title_position=None)`
    :   Get dashboard as pdf
        
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

    `get_dashboard_export_png(self, path, *, include_title=None, include_filters=None, include_ds=None, width=None)`
    :   Get dashboard as png
        
        :param path: Path to save location of png
        :param include_title: Should dashboard title be included in the exported file
        :param include_filters: Should dashboard filters be included in the exported file
        :param include_ds: Should dashboard data source info be included in the exported file
        :param width: Render width in pixels
        :return: The path of the created file

    `get_dashboard_folder_id(self)`
    :   Gets the dashboards folder id
        :return: The folder id of the parent folder of the dashboard

    `get_dashboard_id(self)`
    :   Gets the dashboard's id
        :return: The dashboard's id

    `get_dashboard_shares(self)`
    :   Gets the dashboard shares json
        
        :return: The dashboard shares json

    `get_dashboard_title(self)`
    :   Gets the dashboard's title
        :return: The dashboards title

    `get_dashboard_widgets(self, *, title=None, type=None, subtype=None, fields=None, sort=None, skip=None, limit=None)`
    :   Returns an array of a dashboard’s widgets.
        
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

    `get_dashboards_widget_by_id(self, widget_id, *, fields=None)`
    :   Returns a specific widget (by ID) from a specific dashboard.
        
        @param widget_id: The ID of the widget to get
        @param fields: Whitelist of fields to return for each document. fields Can also define which fields to exclude
            by prefixing field names with -
        @return: A widget object

    `move_to_folder(self, folder)`
    :   Move dashboard to given folder
        :param folder: Folder object to move dashboard to, None to remove from folder
        :return: True if successful

    `post_dashboards_widgets(self, widget)`
    :   Adds the provided widget object to the dashboard
        
        @param widget: widget object to add
        @return: The widget added to the dashboard

    `remove_ghost_widgets(self)`
    :   Removes ghost widgets from dashboard
        
        :return: True

    `share_dashboard_to_user(self, email, rule, subscribe)`
    :   Share a dashboard to a user
        :param email: The email address of the user
        :param rule: The permission of the user on the dashboard (view, edit, etc)
        :param subscribe: true or false, whether to subscribe the user to reports
        :return: The updated share

    `unshare_dashboard_to_user(self, email)`
    :   Unshare a dashboard to a user
        :param email: The email address of the user
        :return: The updated share