from PySense import PySenseBuildTask
from PySense import PySenseDataSet
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

    def get_data_sets(self, *, source=None):
        """Returns the data sets for the model

        Args:
            - (Optional) source: The source of the dataset to filter by (Examples: CSV, SQL)
        """
        ret_arr = []
        for data_set_json in self._data_model_json['datasets']:
            data_set = PySenseDataSet.DataSet(self._py_client, data_set_json)
            if source is not None:
                if source.lower() == data_set.get_source():
                    ret_arr.append(data_set)
            else:
                ret_arr.append(data_set)
        return ret_arr

    def get_schema_json(self):
        if self._py_client.version == SisenseVersion.Version.WINDOWS:
            raise PySenseException.PySenseException('Get schema json not supported on windows')

        if self._schema_json is None:
            query_params = {'datamodelId': self.get_oid(), 'type': 'schema-latest'}
            schema_json = self._py_client.connector.rest_call('get', 'api/v2/datamodel-exports/schema',
                                                              query_params=query_params)
            if schema_json is None:
                raise PySenseException.PySenseException('Schema JSON not found for data model {}'
                                                        .format(self.get_oid()))
            self._schema_json = schema_json
        return self._schema_json

    def start_build(self, build_type, *, row_limit=None):
        """ Initiates a build of the data model

        Only supported on Linux

        Args:
            - build_type: Type of build (schema_changes, by_table, full, publish)
            - (Optional) row_limit: Number of rows to build
        Returns:
            A BuildTask object
        """
        if self._py_client.version != SisenseVersion.Version.LINUX:
            raise PySenseException.PySenseException('Build from API not supported in Windows')

        build_type = build_type.lower()
        if build_type not in ['schema_changes', 'by_table', 'full', 'publish']:
            raise PySenseException.PySenseException('Unsupported build type {}'.format(build_type))

        json_payload = {
            'datamodelId': self.get_oid(),
            'buildType': build_type
        }
        if row_limit is not None:
            json_payload['rowLimit'] = row_limit

        resp_json = self._py_client.connector.rest_call('post', 'api/v2/builds',
                                                        json_payload=json_payload)

        return PySenseBuildTask.BuildTask(self._py_client, resp_json)

    def cancel_build(self):
        """ Cancels all builds for datamodel

        Only supported on Linux

        Args:
            - build_type: Type of build (schema_changes, by_table, full, publish)
            - (Optional) row_limit: Number of rows to build
        Returns:
            A BuildTask object
        """
        if self._py_client.version != SisenseVersion.Version.LINUX:
            raise PySenseException.PySenseException('Cancel build from API not supported in Windows')

        query_params = {
            'datamodelId': self.get_oid()
        }

        self._py_client.connector.rest_call('delete', 'api/v2/builds', query_params=query_params)


