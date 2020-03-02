from PySense import PySense

pyClient = PySense.PySense('localhost:8081', 'nathan.giusti@sisense.com', 'qweQWE123!')
for dashboard in pyClient.get_dashboards():
    dashboard.share_dashboard_to_user('thisistemp@example.com', 'view', 'false')

