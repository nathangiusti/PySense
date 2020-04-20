from PySense import PySense


py_client = PySense.PySense('host', 'username', 'password')

# Get all connections
connections = py_client.get_connections()

# Get all csv connections
csv_connections = py_client.get_connections(provider='CSV')

# Get all csv and postgres connections
csv_connections = py_client.get_connections(provider=['CSV', 'PostgreSQL'])

# Get a single connection by id
connection = py_client.get_connection_by_id('a connection id')

# Update the parameters of a connection and resync it
connection.set_timeout(1000)
connection.set_schema('new schema')
connection.sync_connection()

# Update connection with json patch
connection.update_connection({'timeout': 1000})

# Delete a connection
py_client.delete_connections(connection)

# Delete all my sql connections
py_client.delete_connections(py_client.get_connections(provider=['sql']))