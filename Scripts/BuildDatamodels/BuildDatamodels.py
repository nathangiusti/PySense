"""
Sample script for building data models in sequence.

Linux only

To use this script update the following values:
- wait_time_seconds: How often to poll for the current build status
- build_type: The build type to perform (schema_changes, by_table, full, publish)

Sample Config: https://github.com/nathangiusti/PySense/blob/master/Snippets/SampleConfig.yaml
"""
import time

from PySense import PySense
from PySense import PySenseUtils

config_file_location = 'path//SampleConfig.yaml'
wait_time_seconds = 5
build_type = 'full'

py_client = PySense.authenticate_by_file(config_file_location)

data_models = py_client.get_data_models()

for data_model in PySenseUtils.make_iterable(data_models):
    build_task = data_model.start_build(build_type)
    print('Building data model {}'.format(data_model.get_title()))
    while build_task.get_status() not in ['done', 'failed']:
        time.sleep(wait_time_seconds)
    print('{} build status: {}'.format(data_model.get_title(), build_task.get_status()))

