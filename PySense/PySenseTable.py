class Table:

    def __init__(self, py_client, table_json):
        self._py_client = py_client
        self._table_json = table_json

    def get_config_option(self, config_option):
        """Returns the config option

        Args:
            - config_option: The option to return the value for

        Returns:
            The config option if the option is set, None if the option does not exist
        """

        if self._table_json['configOptions'] is not None and config_option in self._table_json['configOptions']:
            return self._table_json['configOptions'][config_option]
        else:
            return None

    def get_config_options(self):
        """Returns a dictionary of the config options"""
        return self._table_json['configOptions']
