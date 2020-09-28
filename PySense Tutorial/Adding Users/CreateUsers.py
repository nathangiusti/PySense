import csv

from PySense import PySense
from PySense import SisenseRole

py_client = PySense.authenticate_by_file('/Users/nathan.giusti/Documents/PySense/VmConfig.yaml')

groups = ['Designers', 'Viewers', 'Data Designers', 'Greendale']

for group in groups:
    if not py_client.get_groups_by_name(group):
        py_client.add_groups(group)

with open('new_users.csv') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        user_groups = py_client.get_groups_by_name(row['groups'].split('|'))
        py_client.add_user(row['email'], SisenseRole.Role.from_str(row['role']),
                           first_name=row['first_name'], last_name=row['last_name'], groups=user_groups)


