from PySense import PySenseConnection
from PySense import PySenseTable
from PySense import PySenseUtils

class DataSet:

    def __init__(self, py_client, data_set_json, data_model):
        self._py_client = py_client
        self._data_set_json = data_set_json
        self._data_model = data_model

    def get_parent_data_model(self):
        """Returns the data model this data set belongs to as a PySense DataSet"""
        return self._data_model

    def get_oid(self):
        """Returns data set oid"""
        return self._data_set_json['oid']

    def get_full_name(self):
        """Returns data set full name"""
        return self._data_set_json['fullname']

    def get_type(self):
        """Returns data set type"""
        return self._data_set_json['type']

    def get_source(self):
        """Returns source of the dataset"""
        return self.get_full_name().split(":")[0].lower()

    def get_tables(self):
        """Returns the tables"""
        resp = self._py_client.connector.rest_call('get', 'api/v2/datamodels/{}/schema/datasets/{}/tables'
                                                   .format(self._data_model.get_oid(), self.get_oid()))
        ret_arr = []
        for table_json in resp:
            ret_arr.append(PySenseTable.Table(self._py_client, table_json, self))
        return ret_arr

    def get_connection(self):
        """Returns the connection"""
        return PySenseConnection.Connection(self._py_client, self._data_set_json['connection'])

    def set_connection(self, connection):
        """Sets the connection.
        Will update connection on server, local object may still store old connection"""
        connection_json = connection.get_json()
        PySenseUtils.strip_json(connection_json, ['id', '_id', 'owner', 'lastUpdated'])

        json_payload = {'name': self.get_full_name(),
                        'type': self.get_type(),
                        'connection': connection_json}
        self._py_client.connector.rest_call('patch', 'api/v2/datamodels/{}/schema/datasets/{}'
                                            .format(self._data_model.get_oid(), self.get_oid()),
                                            json_payload=json_payload)
        self._sync_data_set()

    def _sync_data_set(self):
        self._data_set_json = self._py_client.connector.rest_call('get', 'api/v2/datamodels/{}/schema/datasets/{}'
                                            .format(self._data_model.get_oid(), self.get_oid()))

    def get_schema(self):
        return self._data_set_json['schema']

