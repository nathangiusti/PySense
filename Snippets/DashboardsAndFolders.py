from PySense import PySense

py_client = PySense.PySense('host', 'username', 'password')

# Get all dashboards
dashboards = py_client.get_dashboards()

# Get dashboards by title and data source
dashboards = py_client.get_dashboards(name='Dashboard Name', data_source_title='Elasticube Name')

# Get dashboard by id
dashboard = py_client.get_dashboard_by_id('mydashboardid')

# Get dashboard name
dashboard.get_name()

# Get dashboard id
dashboard.get_id()

# Get dashboards from a folder
my_folder = py_client.get_folders(name='MyFolder')[0]
py_client.get_dashboards(parent_folder=my_folder)

# Add a dashboard to a folder. 
dashboard.move_to_folder(my_folder)

# Remove a dashboard from a folder
dashboard.move_to_folder()

# Share dashboard to user (user, permission, whether to subscribe to reports)
user = py_client.get_user_by_email('user@email.com')
dashboard.add_share(user, 'View', True)

# Get dashboard data source
ecube = dashboard.get_datasource()

# Unshare dashboard to user
dashboard.remove_shares(user)

# Export a dashboard to png and save locally
dashboard.export_to_png(path='C:\\MyBackUps\\dashboard.png')

# Export a dashboard to pdf and save locally
dashboard.export_to_pdf('A4', 'portrait', 'asis', path='C:\\MyBackUps\\dashboard.pdf')

# Export a dashboard to dash and save locally
dashboard.export_to_dash(path='C:\\MyBackUps\\dashboard.pdf')