import csv

from PySense import PySense

py_client = PySense.authenticate_by_file('/Users/nathan.giusti/Documents/PySense/VmConfig.yaml')
table = 'Category'
column = 'Category ID'
data_type = 'numeric'  # numeric or text
elasticube_name = 'Sample ECommerce'

elasticube = py_client.get_elasticube_by_name(elasticube_name)

# Delete the current rules on the column
try:
    elasticube.delete_data_security_rule(table, column)
except PySense.PySenseException.PySenseException:
    pass

# Create the default security rule
elasticube.add_data_security_rule(table, column, data_type)

with open('DataSecurityRules.csv') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        # Get an array of groups by their name
        groups = py_client.get_groups_by_name(row['groups'].split('|'))

        # Get an array of all the allowed values from the csv
        values = row['values'].split('|')

        if values[0] == 'Nothing':  # Nothing
            elasticube.add_data_security_rule(table, column, data_type, shares=groups)
        elif values[0] == 'Everything':  # Everything
            elasticube.add_data_security_rule(table, column, data_type, shares=groups, all_members=True)
        else:
            elasticube.add_data_security_rule(table, column, data_type, shares=groups, members=values)




