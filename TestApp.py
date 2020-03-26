from PySense import PySense
from PySense import PySenseUtils

pyClient = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
if not pyClient:
    print("Auth error")
    exit(1)

temp = PySenseUtils.get_user_id(pyClient._host, pyClient._token, 'nathan.giusti@sisense.com')
print(temp)




