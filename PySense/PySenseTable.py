class Table:
    """An table in a data model

    Attributes:
        json (JSON): The JSON for this object
        py_client (PySense): The connection to the Sisense server which owns this asset
        dataset (DataSet): The data set this table belongs to
    """

    def __init__(self, py_client, table_json, dataset):
        """

        Args:
            py_client (PySense): The PySense object for the server this asset belongs to
            table_json (JSON): The json for this object
            dataset (DataSet): Parent data set
        """

        self.py_client = py_client
        self.json = table_json
        self.dataset = dataset

    def get_config_option(self, config_option):
        """Returns the config option

        Args:
            config_option (str): The option to return the value for

        Returns:
            str: The config option if the option is set, empty string if no value found
        """

        if self.json['configOptions'] is not None and config_option in self.json['configOptions']:
            return self.json['configOptions'][config_option]
        else:
            return ""

    def update_build_behavior(self, build_json):
        """Update the build behavior for the table

        Args:
            build_json: A json object of build parameters.

        Ex.
        {
            "type": "sync",
            "accumulativeConfig":
            {
                  "column": "string",
                  "type": "lastStored",
                  "lastDays": 0,
                  "keepOnlyDays": 0
            }
        }

        {'type': 'sync', 'accumulativeConfig': None}

        """

        self.json['buildBehavior'] = build_json
        self.py_client.connector.rest_call('patch', 'api/v2/datamodels/{}/schema/datasets/{}/tables/{}'
                                           .format(self.dataset.data_model.get_oid(),
                                                   self.dataset.get_oid(), self.get_oid()),
                                           json_payload=self.json)

    def get_config_options(self):
        """Returns a dictionary of the config options"""

        return self.json['configOptions']

    def get_oid(self):
        """Return oid"""

        return self.json['oid']

    def get_id(self):
        """Return id"""

        return self.json['id']

    def get_type(self):
        """Return type"""

        return self.json['type']

    def get_json(self):
        """Return table json"""

        return self.json

    def get_name(self):
        """Return the table name"""

        return self.json['name']

