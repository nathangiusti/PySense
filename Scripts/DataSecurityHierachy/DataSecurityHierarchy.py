import csv

from PySense import PySense

py_client = PySense.authenticate_by_file('//Users//nathan.giusti//Documents//PySense//VmConfig.yaml')

cube = py_client.get_elasticube_by_name('Data Hierarchy')

# Add default security rules for each level
for i in range(1, 4):
    cube.add_security_rule(
        'Security_Table.csv', 'level' + str(i), 'text'
    )

# This map will track which groups need to get the everything rule for each level.
# Remember each group will have a restriction on one column, and everything access to all other columns.
everything_rule_map = {'level1': [], 'level2': [], 'level3': []}

with open('Security Groups.csv') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        group_name = row['group_name']
        group = py_client.add_groups(group_name)[0]  # Not needed if the group already exists. Just get the group.
        for i in range(1, 4):
            if i == int(row['level']):  # If this is the level to apply security at, we set the security rule
                cube.add_security_rule(
                    'Security_Table.csv', 'level' + str(i), 'text', shares=group, members=[row['value']]
                )
            else:
                everything_rule_map['level' + str(i)].append(group)  # If it isn't, we add it to the everything rule map

# Here at the end we add our everything rules
for i in range(1, 4):
    cube.add_security_rule(
        'Security_Table.csv', 'level' + str(i), 'text', shares=everything_rule_map['level' + str(i)], all_members=True
    )