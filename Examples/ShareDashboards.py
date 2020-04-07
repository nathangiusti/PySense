from PySense import PySense

# Share all dashboards with a new user
pyClient = PySense.authenticate_by_file('C:\\PySenseConfig.yaml')
for dashboard in pyClient.get_dashboards():
    dashboard.share_to_user('thisistemp@example.com', 'view', 'false')

