"""
Sample script for migrating dashboards between servers.

In this example dev_client will be the source of the migration and prod_client will be the target of the migration

Sample configs:

PySenseDev.yaml
host: 'dev.mycomapny.com'
username: 'username'
password: 'password'
os: 'Linux'

PySenseProd.yaml
host: 'prod.mycomapny.com'
username: 'username'
password: 'password'
os: 'Linux'

To use this script update the following values:
- dev_client
    - Authenticate with your dev server by file or inline. See authentication snippet for more examples.
- prod_client
    - Authenticate with your prod server by file or inline. See authentication snippet for more examples.
- dashboard_ids_to_migrate
    - The ids of the dashboard in your development environment that you want to migrate.

"""

from PySense import PySense

dev_client = PySense.authenticate_by_file('C:\\PySense\\PySenseDev.yaml')
prod_client = PySense.authenticate_by_file('C:\\PySense\\PySenseProd.yaml')

dashboard_ids_to_migrate = ['5ebd430b7ff7cf2cbc2641a7', '5dcd92348fcb4538449c4323']

for dashboard_id in dashboard_ids_to_migrate:
    dev_dashboard = dev_client.get_dashboard_by_id(dashboard_id)
    prod_client.add_dashboards(dev_dashboard)
