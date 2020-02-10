"""
Sisense provides the ability to add users via api. But this can become tricky as you need to get alphanumeric ids for
roles and groups. The PySense script does that part for you allowing you to add users with roles like "Viewer" to groups
like "Vendor 1" as PySense will look up those IDs for you.

Look at users.csv for a sample input file to this program which adds users to your Sisense.
"""

import PySense
import csv

if not PySense.authenticate_by_file('C:\\PySenseConfig.yaml'):
    print("Auth error")
    exit(1)

with open("users.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        # email, username, role, first name, last name, groups
        PySense.post_user(row[0], row[1], row[2], row[3], row[4], groups=row[5].split(','))
        # The post_user method also supports additional arguments like preferences and UI settings as JSON objects
