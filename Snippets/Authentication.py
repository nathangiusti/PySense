from PySense import PySense

# Authenticate in line
py_client = PySense.authenticate_by_password('host', 'username', 'password', 'windows')

# Authenticate and turn on debug
py_client = PySense.authenticate_by_password('host', 'username', 'password', 'windows', debug=True)

# Authenticate and disable SSL verification
py_client = PySense.authenticate_by_password('host', 'username', 'password', 'windows', verify=False)

# Authenticate with token
py_client = PySense.authenticate_by_token('host', 'thebearertokenreturnedfromasisenselogincall', 'windows')

# Verify and debug can also be added as values to your config file
# Authenticate by file
# See SampleConfig.yaml
py_client = PySense.authenticate_by_file('SampleConfig.yaml')
