from PySense import PySenseConnection, PySenseTable, PySenseUtils


class DataSet:
    """A Data Set

    Each data set has a connector and a connection to one or more tables.
    A model contains 0 to many data sets.

    Attributes:
        json (JSON): The JSON for this object
        py_client (PySense): The connection to the Sisese server which owns this asset
        data_model (DataModel): The data model this data set belongs to
    """

    def __init__(self, py_client, data_set_json, data_model):
        """

        Args:
            py_client (PySense): The PySense object for the server this asset belongs to
            data_set_json (JSON): The json for this object
            data_model (DataModel): The parent data model of the data set
        """

        self.py_client = py_client
        self.json = data_set_json
        self.data_model = data_model

    def get_oid(self):
        """Returns data set oid"""

        return self.json['oid']

    def get_full_name(self):
        """Returns data set full name"""

        return self.json['fullname']

    def get_type(self):
        """Returns data set type"""

        return self.json['type']

    def get_source(self):
        """Returns source of the dataset"""

        return self.get_full_name().split(":")[0].lower()

    def get_tables(self):
        """Returns the tables

        Returns:
            list[Table]: A list of tables in the data set
        """

        resp = self.py_client.connector.rest_call('get', 'api/v2/datamodels/{}/schema/datasets/{}/tables'
                                                  .format(self.data_model.get_oid(), self.get_oid()))
        ret_arr = []
        for table_json in resp:
            ret_arr.append(PySenseTable.Table(self.py_client, table_json, self))
        return ret_arr

    def get_connection(self):
        """Returns the connection

        Returns:
            Connection: A connection object for the data set
        """

        return PySenseConnection.Connection(self.py_client, self.json['connection'])

    def set_connection(self, connection):
        """Sets a new connection

        Replaces the current connection with the new one. Use to change the source of a table.

        Args:
            connection (Connection): The new Connection object to set for this data set
        """
        connection_json = connection.json
        PySenseUtils.strip_json(connection_json, ['id', '_id', 'owner', 'lastUpdated'])

        json_payload = {'name': self.get_full_name(),
                        'type': self.get_type(),
                        'connection': connection_json}
        self.py_client.connector.rest_call('patch', 'api/v2/datamodels/{}/schema/datasets/{}'
                                           .format(self.data_model.get_oid(), self.get_oid()),
                                           json_payload=json_payload)
        self._sync_data_set()

    def _sync_data_set(self):
        self.json = self.py_client.connector.rest_call('get', 'api/v2/datamodels/{}/schema/datasets/{}'
                                                       .format(self.data_model.get_oid(), self.get_oid()))

    def get_schema(self):
        """Returns the schema for the data set"""
        return self.json['schema']

