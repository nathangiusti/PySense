import json
import os

from PySense import PySense

pyClient = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')

dashboards = pyClient.get_dashboards(name='PySense')
for dashboard in dashboards:
    dashboard.get_dashboard_export_dash("c:\\PySense\\dashfiles\\{}.dash".format(dashboard.get_dashboard_id()))

for filename in os.listdir('c:\\PySense\\dashfiles'):
    with open(os.path.join('c:\\PySense\\dashfiles', filename), "r") as file:
        dash_file = file.read()
    dashboard = pyClient.post_dashboards(json.loads(dash_file))
    dashboard.move_to_folder(pyClient.get_folders(name='PySense')[0])


