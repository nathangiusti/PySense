from PySense import PySense

py_client = PySense.PySense('host', 'username', 'password')

# Get all groups
groups = py_client.get_groups()

# Get all groups by name
# Can add multiple arguments, see documentation for full list
groups = py_client.get_groups(name='MyGroupName')

# Create groups by name. 
group_names = ['Group 1', 'Group 2']
new_groups = py_client.add_groups(groups)

# Delete groups
py_client.delete_groups(new_groups)

# Delete group by name
groups_to_delete = py_client.get_groups(name='GroupsToDelete')
py_client.delete_groups(groups_to_delete)

# Add user
py_client.add_user('user@email.com', 'Viewer')

# Add user with more details. 
# Can add multiple arguments, see documentation for full list
py_client.add_user('user@email.com', 'Data Designer', first_name='John', last_name='Doe')

# Get all users
users = py_client.get_users()

# Get all users by first name
# Can add multiple arguments, see documentation for full list
users = py_client.get_users(first_name='John')

# Update user
user = py_client.connector.get_user_by_email('myuser@email.com')
user.update(first_name='New First Name', last_name='New Last Name')

# Delete user
users = py_client.get_users(user_name='deleted_user@email.com')
py_client.delete_users(users)
