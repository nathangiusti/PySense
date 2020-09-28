from PySense import PySense
from PySense import SisenseRole

py_client = PySense.authenticate_by_password('host', 'username', 'password', 'windows')

py_client = PySense.authenticate_by_password('host', 'username', 'password', 'windows', debug=True, verify=False)

py_client = PySense.authenticate_by_token('host', 'thebearertokenreturnedfromasisenselogincall', 'windows')

py_client = PySense.authenticate_by_file('SampleConfig.yaml')

print(SisenseRole.Role.from_str('Viewer    '))
print(SisenseRole.Role.from_str('   viewer'))
print(SisenseRole.Role.from_str('VIEWER'))
print(SisenseRole.Role.from_str('cOnSumEr'))

role = SisenseRole.Role.from_str('Viewer')

print(py_client.get_role_id(role))