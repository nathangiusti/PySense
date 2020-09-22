"""
Sample script for creating users

We will read from the new_users.csv and create new users.

What to do when a user is to be added to a group that does not exist
create_group:
- True: Create a new group with the group name
- False: Throw an error

What to do when a user to be added is already found
action_on_found_user:
- 'Update': Update the user to the settings
- 'Skip': Do nothing and continue to next user
- 'Error': Throw an error

Ensure:
- All groups have unique names. If two groups have the same name, this script will grab one at random
- There are not trailing or leading white space in your csv

PySense does not currently support Active Directory

Sample Config: https://github.com/nathangiusti/PySense/blob/master/Snippets/SampleConfig.yaml
"""

import csv

from PySense import PySense
from PySense import SisenseRole

py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')

create_group = False
action_on_found_user = 'Update'


def get_groups(group_names):
    if not group_names or not group_names[0]:
        return []
    ret_arr = []
    for group_name in group_names:
        groups = py_client.get_groups_by_name(group_name)
        if len(groups) == 0:
            if create_group:
                group = py_client.add_groups(group_name)
            else:
                print('No group with name {} found'.format(group_name))
                exit(1)
        else:
            group = groups[0]
        ret_arr.append(group)
    return ret_arr


with open('new_users.csv') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        user_groups = get_groups(row['groups'].split('|'))
        user = py_client.get_user_by_email(row['email'])
        if user is not None:
            if action_on_found_user == 'Update':
                user.update(role_name=SisenseRole.Role.from_str(row['role']), first_name=row['first_name'],
                            last_name=row['last_name'], groups=user_groups)
            elif action_on_found_user == 'Skip':
                continue
            else:
                print('No user with email {} found'.format(row['email']))
                exit(1)
        else:
            py_client.add_user(row['email'], SisenseRole.Role.from_str(row['role']),
                               first_name=row['first_name'], last_name=row['last_name'], groups=user_groups)


