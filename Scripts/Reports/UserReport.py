"""
Get's all users and prints the following to a csv:
Username, email, full name, groups, role, last active, days since last active

Set the report name by modifying the report_name variable.
"""

import csv
from datetime import datetime
from PySense import PySense

py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')

report_name = 'UserReport.csv'
users = py_client.get_users()

with open(report_name, 'w', newline='') as csv_file:
    user_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    user_writer.writerow(
        ['Username', 'Email', 'Name', 'Groups', 'Role', 'Last Active', 'Days Since Last Active']
    )
    for user in users:
        group_list_string = ""
        for group in user.get_groups():
            group_list_string = group_list_string + ' ' + group.get_title()
        full_name = user.get_first_name() + ' ' + user.get_last_name()
        user_writer.writerow([
            user.get_user_name(),
            user.get_email(),
            full_name.strip(),
            group_list_string.strip(),
            user.get_role(),
            user.get_last_login(),
            (datetime.now() - user.get_last_login()).days + 1]
        )
