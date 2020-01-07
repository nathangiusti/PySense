"""
Sisense does not currently have any built in versioning support.
As a work around we can upload all of our dashboards to S3.

This script grabs all dashboards in an instance and uploads them to an S3 bucket.
"""

import PySense
import PySenseS3

# Authenticate with a config file. See SampleConfig.yaml for example
if not PySense.authenticate_by_file('C:\\PySenseConfig.yaml'):
    print("Auth error")
    exit(1)

# Turn on versioning for bucket. This is optional. It only needs to be done once. It can be done directly through AWS.
PySenseS3.configure_versioning('nathangiusti-east1', True)

# Pass in additional parameters to get_dashboards to narrow, otherwise it will get all dashboards
dashboards = PySense.get_dashboards()
for dashboard in dashboards:
    # The last argument is the file's name on S3. I suggest using oid as it is unique and constant dashboard identifier
    PySenseS3.upload_dashboard('nathangiusti-east1', dashboard, dashboard['oid'])
