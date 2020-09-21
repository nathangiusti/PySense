from PySense import PySense

py_client = PySense.authenticate_by_password('host', 'username', 'password', 'windows')

py_client = PySense.authenticate_by_password('host', 'username', 'password', 'windows', debug=True, verify=False)

py_client = PySense.authenticate_by_token('host', 'thebearertokenreturnedfromasisenselogincall', 'windows')

py_client = PySense.authenticate_by_file('SampleConfig.yaml')

print(py_client.get_role_id('Viewer'))
