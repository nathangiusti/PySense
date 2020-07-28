"""
Backs up all dashboards to a folder. Dashboards will be named <dashboard_id>.dash and placed in the backup folder.

config_file_location: The full path including file name of your config file
path_to_backup: A path to your backup directory. End the path with '\\' as seen below.

"""
from PySense import PySense

config_file_location = 'C:\\PySense\\PySenseConfig.yaml'
path_to_backup = 'C:\\PySense\\Backups\\'

py_client = PySense.authenticate_by_file(config_file_location)

for dashboard in py_client.get_dashboards():
    dashboard.export_to_dash(path=path_to_backup + '{}.dash'.format(dashboard.get_id()))