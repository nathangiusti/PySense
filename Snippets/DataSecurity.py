from PySense import PySense

py_client = PySense.authenticate_by_file('SampleConfig.yaml')

elasticube = py_client.get_elasticube_by_name('CubeTitle')

# Add default Nothing rule for column
elasticube.add_data_security_rule('table_name', 'column_name', 'numeric')

# Add default rule for some values
elasticube.add_data_security_rule('table_name', 'column_name', 'numeric', members=['1', '2'])

# Add security rule for all users
users = py_client.get_users()
elasticube.add_data_security_rule('table_name', 'column_name', 'numeric', shares=users, members=['3', '4'])

# Give group 'Everything' Rule
groups = py_client.get_groups(name='Admins')
elasticube.add_data_security_rule('table_name', 'column_name', 'numeric', all_members=True, shares=groups)

# Get all data security rules
rules = elasticube.get_data_security()

# Get all rules for a table/column
rules = elasticube.get_data_security_by_table_column('table_name', 'column_name')

# Delete all the rules for a table/column
elasticube.delete_data_security_rule('table_name', 'column_name')