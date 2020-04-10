from PySense import PySense

# Authenticate
py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')

# Get plugins returns an array. Use the search parameter to filter by name. 
my_plugin = py_client.get_plugins(search='MyPluginName')[0]

# Set plugin to disabled
my_plugin.set_plugin_enabled(False)

print('{} v{} enabled set to {}'.format(my_plugin.get_name(), my_plugin.get_version(), my_plugin.get_is_enabled()))
