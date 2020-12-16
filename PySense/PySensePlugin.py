from PySense import PySenseUtils


class Plugin:
    """A plugin

    A plugin currently installed on the Sisense server

    Attributes:
        json (JSON): The JSON for this object
        py_client (PySense): The connection to the Sisense server which owns this asset
    """

    def __init__(self, py_client, plugin_json):
        """

        Args:
            py_client (PySense): The PySense object for the server this asset belongs to
            plugin_json (JSON): The json for this object
        """

        self.py_client = py_client
        self.json = plugin_json

    def get_name(self):
        """Get the plugins name."""

        return self.json['name']

    def get_last_update(self):
        """Get the plugins last update time.

        Returns:
            datetime: The time the plugin was last updated
        """

        return PySenseUtils.sisense_time_to_python(self.json['lastUpdate'])

    def get_version(self):
        """Get the plugins version."""

        return self.json['version']

    def get_is_enabled(self):
        """Returns whether the plugin is enabled."""

        return self.json['isEnabled']

    def set_plugin_enabled(self, enabled):
        """Enable/disable the plugin

        Args:
            enabled (bool): True to enable. False to disable
        """

        self.json['isEnabled'] = enabled
        resp_json = self.py_client.connector.rest_call('patch', 'api/v1/plugins', json_payload=[self.json])
        self.json = resp_json[0]
