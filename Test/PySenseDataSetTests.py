import unittest

from PySense import PySense


class PySenseDataSetTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('//Users//nathan.giusti//Documents//PySense//PySenseLinux.yaml')
        assert cls.py_client.get_elasticube_by_name('PySense') is not None
        cls.data_set = cls.py_client.get_elasticube_by_name('PySense').get_model().get_data_sets()[0]

    def test_getters(self):
        assert self.data_set.get_source() is not None
        assert self.data_set.get_oid() is not None
        assert self.data_set.get_full_name() is not None
        assert self.data_set.get_tables() is not None
        assert self.data_set.get_type() is not None

    def test_connections(self):
        connection = self.data_set.get_connection()
        connection.update_connection({'timeout': 400})
        self.data_set.set_connection(connection)
        new_connection = self.data_set.get_connection()
        assert new_connection.get_json()['timeout'] == 400
        new_connection.update_connection({'timeout': 300})
        self.data_set.set_connection(new_connection)
        new_connection = self.data_set.get_connection()
        assert new_connection.get_json()['timeout'] == 300


if __name__ == '__main__':
    unittest.main()
