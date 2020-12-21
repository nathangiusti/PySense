"""
Dashboard backup and removal script.

This file will delete the dashboards with id's listed in dash_file.txt

Option to back up deleted dashboards. Deleted dashboards will be stored as {dashboard_id}.dash
There is a metadata file that will be written containing a mapping of dashboard ids to titles and owners

config_file_location: The full path including file name of your config file
dash_file: Path to file containing all dashboard ids to be deleted, one per line
backup_dashboards: If true, will backup deleted dashboards to a directory
path_to_backup: A path to your backup directory. Only needed if backing up dashboards
"""
from PySense import PySense

config_file_location = 'path//SampleConfig.yaml'
path_to_backup = 'path//Backups//'
dash_file = 'path//Backups//DashToDelete.txt'
backup_dashboards = True

py_client = PySense.authenticate_by_file(config_file_location)

dash_list = open(dash_file, "r")
lines = []
for line in dash_list:
    dashboard = py_client.get_dashboard_by_id(line.strip(), admin_access=True)
    if backup_dashboards:
        lines.append("{},{},{}\n".format(dashboard.get_oid(), dashboard.get_title(), dashboard.get_owner().get_email()))
        dashboard.export_to_dash(path='{}{}.dash'.format(path_to_backup, dashboard.get_oid()), admin_access=True)
    py_client.delete_dashboards(dashboard, admin_access=True)

if backup_dashboards:
    with open("MetaData.csv", "w") as out_file:
        out_file.writelines(lines)


