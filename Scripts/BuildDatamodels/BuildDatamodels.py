"""
Sample script for building data models in sequence.

Linux only

To use this script update the following values:
- wait_time_seconds: How often to poll for the current build status
- build_type: The build type to perform (schema_changes, by_table, full, publish)

"""
import time

from PySense import PySense
from PySense import PySenseUtils

wait_time_seconds = 5
build_type = 'full'

py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseLinux.yaml')

data_models = py_client.get_data_models()

for data_model in PySenseUtils.make_iterable(data_models):
    build_task = data_model.start_build(build_type)
    print('Building data model {}'.format(data_model.get_title()))
    while build_task.get_status() not in ['done', 'failed']:
        time.sleep(wait_time_seconds)
    print('{} build status: {}'.format(data_model.get_title(), build_task.get_status()))

