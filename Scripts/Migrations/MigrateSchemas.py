"""
Sample script for migrating schemas between servers.

Schema migration by API is only support on Linux.

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
- data_model_to_migrate
    - The name of the data model in your development environment that you want to migrate.
- overwrite
    - If true, will replace an existing data model named by data_model_to_overwrite
    - If false, will create a new data model on the server
- data_model_to_overwrite
    - The title of the data model in prod to update. Required if overwrite is true
- new_title
    - The new title of the data model in prod
    - If overwrite is true, this will not be used
    - If overwrite is false and this field is left blank, the dev name will be used

"""

from PySense import PySense

dev_config_file_location = 'path//PySenseDev.yaml'
prod_config_file_location = 'path//PySenseProd.yaml'

dev_client = PySense.authenticate_by_file(dev_config_file_location)
prod_client = PySense.authenticate_by_file(prod_config_file_location)

data_model_to_migrate = 'Dev Data Model'
data_model_to_overwrite = 'Prod Data Model'

new_title = None
overwrite = True

dev_data_model = dev_client.get_data_models(title=data_model_to_migrate)

if overwrite:
    prod_data_model = prod_client.get_data_models(title=data_model_to_overwrite)
    prod_client.add_data_model(dev_data_model, target_data_model=prod_data_model)
else:
    title = new_title if new_title is not None else None
    prod_client.add_data_model(dev_data_model, title=title)
