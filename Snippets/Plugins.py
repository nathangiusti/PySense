from PySense import PySense

py_client = PySense.PySense('host', 'username', 'password', 'version')

# Get all plugins
my_plugins = py_client.get_plugins()

# Get plugin by name 
my_plugin = py_client.get_plugins(search='MyPluginName')[0]

# Set plugin to disabled
my_plugin.set_plugin_enabled(False)

# Enable plugin
my_plugin.set_plugin_enabled(True)