"""
Get's the number of recent viewers for a list of dashboards and writes the results to csv.

recency_in_days: The number of days ago that is considered recent.
report_name: The path to save the report to, including the file name.
config_file_location: The location of the config file with your Sisense credentials.
"""

import csv
import datetime

from PySense import PySense

"""Configuration"""
recency_in_days = 30
report_name = '/Users/Documents/Reports/DashboardRecencyReport.csv'
config_file_location = '/Users/Documents/PySense/Config.yaml'
"""End Configuration"""

py_client = PySense.authenticate_by_file(config_file_location)

comp_date = datetime.date.today() - datetime.timedelta(days=recency_in_days)
report_map = {}

owner_dashboards = py_client.get_dashboards_admin(dashboard_type='owner')
length = len(owner_dashboards)
x = 0
for owner_dashboard in owner_dashboards:
    viewer_dashboards = py_client.get_dashboards_admin(dash_id=owner_dashboard.get_id())
    for dashboard in viewer_dashboards:
        if dashboard.get_id() in report_map:
            if dashboard.get_last_opened() is not None:
                if dashboard.get_last_opened().date() > comp_date:
                    report_map[dashboard.get_id()][3] = report_map[dashboard.get_id()][3] + 1
                if dashboard.get_last_opened().date() > report_map[dashboard.get_id()][4]:
                    report_map[dashboard.get_id()][4] = dashboard.get_last_opened().date()
        else:
            if dashboard.get_last_opened() is not None:
                val = 1 if dashboard.get_last_opened().date() > comp_date else 0
                report_map[dashboard.get_id()] = [dashboard.get_title(), dashboard.get_id(),
                                                  dashboard.get_owner().get_email(), val,
                                                  dashboard.get_last_opened().date()]
            else:
                report_map[dashboard.get_id()] = [dashboard.get_title(), dashboard.get_id(),
                                                  dashboard.get_owner().get_email(), 0,
                                                  datetime.datetime(1970, 1, 1).date()]
    x = x + 1
    print("{}/{}".format(x, length), end='\r')


with open(report_name, 'w', newline='') as csv_file:
    dashboard_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    dashboard_writer.writerow(
        ['Dashboard Name', 'Dashboard ID', 'Owner', 'Recent Users', 'Last Opened']
    )
    for report in report_map.values():
        dashboard_writer.writerow(report)
