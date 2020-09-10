from PySense import PySenseDataModel
from PySense import PySenseUtils
from PySense import SisenseVersion


class DataModelMixIn:
    def add_data_model(self, data_model, *, title=None, target_data_model=None):
        """Adds a new data model to the instance.

        Sisense does not support this in Windows

        Can be used to update an existing data model by adding it to target data model.

        To add a new model with a new title
        add_data_model(model_to_add, title='New Title')

        To update an existing model
        add_data_model(new_data_model, target_data_model=old_data_model)

        If updating an existing data model, no modifications to title will happen.

        Args:
            data_model: The PySense DataModel object to import
            title: (optional) Title to give the data model
            target_data_model: (optional) The data model to update.
        """
        self._validate_version(SisenseVersion.Version.LINUX, 'add_data_model')

        target_data_model_id = target_data_model.get_oid() if target_data_model is not None else None

        query_params = {'title': title, 'datamodelId': target_data_model_id}
        data_model_json = self.connector.rest_call('post', 'api/v2/datamodel-imports/schema',
                                                   query_params=query_params, json_payload=data_model.get_schema_json())

        return PySenseDataModel.DataModel(self, data_model_json)

    def get_data_models(self, *, title=None, fields=None, sort=None, limit=None, skip=None):
        """Gets data model schemas

        Sisense does not support this in Windows

        If fields is specified, PySense may experience issues.

        To get all data models:
        get_data_models()

        To get a data model called PySense:
        get_data_models(title='PySense')

        Args:
            title: (optional) Datamodel Title to search for
            fields: (optional) A whitelist of fields to return for each object in the response.
            sort: (optional) A field by which the results should be sorted.
                Results will be sorted in ascending order by default, or descending if the field name is prefixed by -.
            limit: (optional) Number of results to be returned from the data set.
                This field must be used with the skip parameter, and is intended for paging.
            skip: (optional) Number of results to skip from the start of the data set.
                This parameter must be used with the limit parameter, and is intended for paging.

        Returns:
            If title is specified, a single data model will be returned if a matching data model is found,
            otherwise None
            If title is not specified an array will be returned.

        """
        self._validate_version(SisenseVersion.Version.LINUX, 'get_data_models')

        query_params = {
            'title': title,
            'fields': fields,
            'sort': sort,
            'limit': limit,
            'skip': skip
        }

        data_models = self.connector.rest_call('get', 'api/v2/datamodels/schema', query_params=query_params)
        if title is not None:
            if data_models is not None and len(data_models) > 0:
                return PySenseDataModel.DataModel(self, data_models)
            else:
                return None
        else:
            ret_arr = []
            for data_model in data_models:
                ret_arr.append(PySenseDataModel.DataModel(self, data_model))
            return ret_arr

    def delete_data_model(self, data_models):
        """Deletes the given data models

        Args:
            data_models: One to many data models to delete
        """
        self._validate_version(SisenseVersion.Version.LINUX, 'delete_data_model')

        for data_model in PySenseUtils.make_iterable(data_models):
            self.connector.rest_call('delete', 'api/v2/datamodels/{}'.format(data_model.get_oid()))

    def import_schema(self, path, *, title=None, target_data_model=None):
        """Import schema file from path

        Sisense does not support this in Windows

        Can be used to update an existing data model by adding it to target data model.

        To add a new model with a new title
        add_data_model(path, title='New Title')

        To update an existing model
        add_data_model(path, target_data_model=old_data_model)

        If updating an existing data model, no modifications to title will happen.

        Args:
            path: The path to the schema smodel file
            title: (optional) Title to give the data model
            target_data_model: (optional) The data model to update.
        """
        self._validate_version(SisenseVersion.Version.LINUX, 'import_schema')

        target_data_model_id = target_data_model.get_oid() if target_data_model is not None else None

        query_params = {'title': title, 'datamodelId': target_data_model_id}
        data_model_json = self.connector.rest_call('post', 'api/v2/datamodel-imports/schema',
                                                   query_params=query_params, json_payload=PySenseUtils.read_json(path))

        return PySenseDataModel.DataModel(self, data_model_json)
