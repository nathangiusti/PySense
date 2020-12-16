from PySense import PySenseDataModel, PySenseUtils, SisenseVersion


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
            data_model (DataModel): The PySense DataModel object to import
            title (str): (Optional) Title to give the data model
            target_data_model (DataModel): (Optional) The data model to update.

        Returns:
            DataModel: The newly added data model
        """

        PySenseUtils.validate_version(self, SisenseVersion.Version.LINUX, 'add_data_model')

        target_data_model_id = target_data_model.get_oid() if target_data_model is not None else None

        query_params = {'title': title, 'datamodelId': target_data_model_id}
        data_model_json = self.connector.rest_call('post', 'api/v2/datamodel-imports/schema',
                                                   query_params=query_params, json_payload=data_model.get_schema_json())

        return PySenseDataModel.DataModel(self, data_model_json)

    def get_data_models(self, *, title=None, fields=None, sort=None, limit=None, skip=None):
        """Gets data model schemas

        Linux Only

        If fields is specified, PySense may experience issues.

        To get all data models:
        get_data_models()

        To get a data model called PySense:
        get_data_models(title='PySense')

        Args:
            title (str): (Optional) Datamodel Title to search for
            fields (list[str]): (Optional) A whitelist of fields to return for each object in the response.
            sort (str): (Optional) A field by which the results should be sorted.
                Results will be sorted in ascending order by default, or descending if the field name is prefixed by -.
            limit (int): (Optional) Number of results to be returned from the data set.
                This field must be used with the skip parameter, and is intended for paging.
            skip (int): (Optional) Number of results to skip from the start of the data set.
                This parameter must be used with the limit parameter, and is intended for paging.

        Returns:
            list[DataModel]: The data models found

        """
        PySenseUtils.validate_version(self, SisenseVersion.Version.LINUX, 'get_data_models')

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
                return [PySenseDataModel.DataModel(self, data_models)]
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
        PySenseUtils.validate_version(self, SisenseVersion.Version.LINUX, 'delete_data_model')

        for data_model in PySenseUtils.make_iterable(data_models):
            self.connector.rest_call('delete', 'api/v2/datamodels/{}'.format(data_model.get_oid()))

    def import_schema(self, path, *, title=None, target_data_model=None):
        """Import schema file from path

        Sisense does not support this in Windows

        Can be used to update an existing data model by adding it to target data model.

        To add a new model with a new title
        import_schema(path, title='New Title')

        To update an existing model
        import_schema(path, target_data_model=old_data_model)

        If updating an existing data model, no modifications to title will happen.

        Args:
            path: The path to the schema smodel file
            title: (Optional) Title to give the data model
            target_data_model: (Optional) The data model to update.
        """
        PySenseUtils.validate_version(self, SisenseVersion.Version.LINUX, 'import_schema')

        target_data_model_id = target_data_model.get_oid() if target_data_model is not None else None

        query_params = {'title': title, 'datamodelId': target_data_model_id}
        data_model_json = self.connector.rest_call('post', 'api/v2/datamodel-imports/schema',
                                                   query_params=query_params, json_payload=PySenseUtils.read_json(path))

        return PySenseDataModel.DataModel(self, data_model_json)

    def import_sdata(self, path, *, title=None, target_data_model=None):
        """Import sdata file from path

        Linux only

        Can be used to update an existing data model by adding it to target data model.

        To add a new model with a new title
        import_sdata(path, title='New Title')

        To update an existing model
        import_sdata(path, target_data_model=old_data_model)

        If updating an existing data model, no modifications to title will happen.

        This method sometimes throws 500 errors.
        If it does, try the file from UI to verify it is a PySense issue or a Sisense issue

        Args:
            path: The path to the schema smodel file
            title: (Optional) Title to give the data model
            target_data_model: (Optional) The data model to update.
        """
        PySenseUtils.validate_version(self, SisenseVersion.Version.LINUX, 'import_schema')

        target_data_model_id = target_data_model.get_oid() if target_data_model is not None else None

        query_params = {'title': title, 'datamodelId': target_data_model_id}
        data_model_json = self.connector.rest_call('post', 'api/v2/datamodel-imports/stream/full',
                                                   query_params=query_params, file=path)

        return PySenseDataModel.DataModel(self, data_model_json)