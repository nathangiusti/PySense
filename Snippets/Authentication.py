from PySense import PySense

# Authenticate in line
py_client = PySense.PySense('host', 'username', 'password')

# Authenticate by file
# See SampleConfig.yaml
py_client = PySense.authenticate_by_file('SampleConfig.yaml')

# Authenticate and turn on debug
py_client = PySense.PySense('host', 'username', 'password', debug=True)

# Authenticate and disable SSL verification
py_client = PySense.PySense('host', 'username', 'password', verify=False)

# Verify and debug can also be added as values to your config file
