from PySense import PySense

# Authenticate in line
py_client = PySense.PySense('host', 'username', 'password', 'version')  # os is either 'Windows' or 'Linux'

# Authenticate and turn on debug
py_client = PySense.PySense('host', 'username', 'password', 'windows', debug=True)

# Authenticate and disable SSL verification
py_client = PySense.PySense('host', 'username', 'password', 'windows', verify=False)

# Verify and debug can also be added as values to your config file
# Authenticate by file
# See SampleConfig.yaml
py_client = PySense.authenticate_by_file('SampleConfig.yaml')


