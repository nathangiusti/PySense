from PySense import PySenseTable


class DataSet:

    def __init__(self, py_client, data_set_json):
        self._py_client = py_client
        self._data_set_json = data_set_json

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
        ret_arr = []
        for table_json in self._data_set_json['schema']['tables']:
            ret_arr.append(PySenseTable.Table(self._py_client, table_json))
        return ret_arr

