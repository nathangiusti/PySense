from PySense import PySense

# Authenticate in line
py_client = PySense.PySense('host', 'username', 'password', debug=False)

# Authenticate by file
# See SampleConfig.yaml
py_client = PySense.authenticate_by_file('SampleConfig.yaml')