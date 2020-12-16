from PySense import PySenseBuildTask, PySenseDataSet, PySenseException, PySenseUtils, SisenseVersion


class DataModel:
    """A Data Model

    A data model can represent either an Elasticube or a live model.
    Each data model has 0 to many data sets which define the tables in the data model

    Attributes:
        json (JSON): The JSON for this object
        py_client (PySense): The connection to the Sisense server which owns this asset
    """

    def __init__(self, py_client, data_model_json):
        """

        Args:
            py_client (PySense): The PySense object for the server this asset belongs to
            data_model_json (JSON): The json for this object
        """

        self.py_client = py_client
        self.json = data_model_json

    def get_title(self):
        """Returns the data models title"""

        return self.json['title']

    def get_oid(self):
        """Returns the data models oid"""

        return self.json['oid']

    def get_data_sets(self, *, source=None):
        """Returns the data sets for the model

        Args:
            source (str): (Optional) The source of the dataset to filter by (Examples: CSV, SQL)

        Returns:
            list[DataSet]: The data sets in the model
        """

        ret_arr = []
        for data_set_json in self.json['datasets']:
            data_set = PySenseDataSet.DataSet(self.py_client, data_set_json, self)
            if source is not None:
                if source.lower() == data_set.get_source():
                    ret_arr.append(data_set)
            else:
                ret_arr.append(data_set)
        return ret_arr

    def start_build(self, build_type, *, row_limit=None):
        """Initiates a build of the data model

        Only supported on Linux

        Args:
            build_type (str): Type of build (schema_changes, by_table, full, publish)
            row_limit (int): (Optional) Number of rows to build
        Returns:
            BuildTask: The build task object for the build
        """

        PySenseUtils.validate_version(self.py_client, SisenseVersion.Version.LINUX, 'start_build')

        build_type = build_type.lower()
        if build_type not in ['schema_changes', 'by_table', 'full', 'publish']:
            raise PySenseException.PySenseException('Unsupported build type {}'.format(build_type))

        json_payload = {
            'datamodelId': self.get_oid(),
            'buildType': build_type
        }
        if row_limit is not None:
            json_payload['rowLimit'] = row_limit

        resp_json = self.py_client.connector.rest_call('post', 'api/v2/builds',
                                                       json_payload=json_payload)

        return PySenseBuildTask.BuildTask(self.py_client, resp_json)

    def cancel_build(self):
        """ Cancels all builds for data model

        Only supported on Linux
        """

        PySenseUtils.validate_version(self.py_client, SisenseVersion.Version.LINUX, 'cancel_build')

        query_params = {
            'datamodelId': self.get_oid()
        }

        self.py_client.connector.rest_call('delete', 'api/v2/builds', query_params=query_params)

    def export_to_smodel(self, path):
        """Download data model as an smodel file.

        Only supported on Linux

        Args:
            path (str): Path to save location of the smodel file.

        Returns:
            str: The path of the created file
        """

        PySenseUtils.validate_version(self.py_client, SisenseVersion.Version.LINUX, 'export_to_smodel')

        query_params = {
            'datamodelId': self.get_oid(),
            'type': 'schema-latest'
        }
        self.py_client.connector.rest_call('get', '/api/v2/datamodel-exports/schema',
                                           query_params=query_params, path=path)

        return path

    def export_to_sdata(self, path):
        """Download data model as an sdata file.

        Only supported on Linux

        Args:
            path (str): Path to save location of the sdata file.

        Returns:
            str: The path of the created file
        """

        PySenseUtils.validate_version(self.py_client, SisenseVersion.Version.LINUX, 'export_to_sdata')

        query_params = {
            'datamodelId': self.get_oid()
        }
        self.py_client.connector.rest_call('get', '/api/v2/datamodel-exports/stream/full',
                                           query_params=query_params, path=path, raw=True)

        return path
