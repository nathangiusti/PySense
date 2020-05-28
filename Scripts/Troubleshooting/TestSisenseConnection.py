"""
This script is to be used to validate your configuration to your Sisense server independent of PySense.

Set the host, username, and password.

If you are getting SSL errors and wish to disable SSL, you can set verify to False.

If this script returns an error
    - Ensure host, username, and password are correct
    - Use another tool like Postman to make the same call and see if it is successful
    - Contact your IT team and verify the network is configured correctly
    - File a ticket with the Technical Solutions Team concerning connecting to your Sisense server

"""
import requests

host = 'http://localhost:8081'
username = 'your_username'
password = 'your_password'
verify = True

data = {'username': username, 'password': password}
response = requests.post('{}/api/v1/authentication/login'.format(host), verify=verify, data=data)

if response.status_code not in [200, 201, 204]:
    print('ERROR: {}: {}\nURL: {}'.format(response.status_code, response.content, response.url))
else:
    print('Success')
    print(response.content)
