import unittest

from PySense import PySense


class PySenseDataSetTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('resources//LinuxConfig.yaml')
        cls.data_set = cls.py_client.get_data_models(title='PySense')[0].get_data_sets(source='CSV')[0]

    def test_getters(self):
        assert self.data_set.get_source() is not None
        assert self.data_set.get_oid() is not None
        assert self.data_set.get_full_name() is not None
        assert self.data_set.get_tables() is not None
        assert self.data_set.get_type() is not None

    def test_connections(self):
        connection = self.data_set.get_connection()
        connection.json['timeout'] = 400
        self.data_set.set_connection(connection)
        new_connection = self.data_set.get_connection()
        assert new_connection.json['timeout'] == 400
        new_connection.json['timeout'] = 300
        self.data_set.set_connection(new_connection)
        new_connection = self.data_set.get_connection()
        assert new_connection.json['timeout'] == 300


if __name__ == '__main__':
    unittest.main()
