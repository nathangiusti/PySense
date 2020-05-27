"""
Get's all the table configuration options for an elasticube

Set the elasticube_name variable
"""

from PySense import PySense

elasticube_name = 'Sample ECommerce'

py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseLinux.yaml')

cube = py_client.get_elasticube_by_name(elasticube_name)
print(cube.get_name())
for data_set in cube.get_model().get_data_sets():
    print(data_set.get_full_name())
    for table in data_set.get_tables():
        print(table.get_config_options())

# Linux Only
data_model = py_client.get_data_models(title=elasticube_name)
print(data_model.get_title())
for data_set in data_model.get_data_sets():
    print(data_set.get_full_name())
    for table in data_set.get_tables():
        print(table.get_config_options())