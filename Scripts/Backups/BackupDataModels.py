"""
Backs up all data models to a folder. Data models will be named <data model title>.smodel and placed in the backup folder.

config_file_location: The full path including file name of your config file
path_to_backup: A path to your backup directory. End the path with '\\' as seen below.

"""
from PySense import PySense

config_file_location = 'path//SampleConfig.yaml'
path_to_backup = 'path//Backups//'

py_client = PySense.authenticate_by_file(config_file_location)

data_models = py_client.get_data_models()

for data_model in data_models:
    data_model.export_to_smodel(path_to_backup + data_model.get_title() + '.smodel')