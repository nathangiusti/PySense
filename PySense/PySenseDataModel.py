from PySense import PySenseException
from PySense import SisenseVersion


class DataModel:

    def __init__(self, py_client, data_model_json):
        self._py_client = py_client
        self._data_model_json = data_model_json
        self._schema_json = None
        if py_client.version == SisenseVersion.Version.LINUX:
            self._schema_json = self.get_schema_json()

    def get_json(self):
        """Returns the data model's JSON"""
        return self._data_model_json
    
    def get_title(self):
        """Returns the data models title"""
        return self._data_model_json['title']
    
    def get_oid(self):
        """Returns the data models oid"""
        return self._data_model_json['oid']
    
    def get_schema_json(self):
        if self._schema_json is None:
            query_params = {'datamodelId': self.get_oid(), 'type': 'schema-latest'}
            schema_json = self._py_client.connector.rest_call('get', 'api/v2/datamodel-exports/schema', 
                                                              query_params=query_params)
            if schema_json is None:
                raise PySenseException.PySenseException('Schema JSON not found for data model {}'
                                                        .format(self.get_oid()))
            self._schema_json = schema_json
        return self._schema_json
