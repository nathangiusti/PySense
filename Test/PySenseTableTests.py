import unittest

from PySense import PySense


class PySenseTableTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('//Users//nathan.giusti//Documents//PySense//PySenseLinux.yaml')
        cls.table = cls.py_client.get_elasticube_by_name('PySense').get_model().get_data_sets()[0].get_tables()[0]

    def test_getters(self):
        assert self.table.get_config_option('hasHeader') is not None
        options = self.table.get_config_options()
        assert options is not None
        assert options['hasHeader'] == self.table.get_config_option('hasHeader')
        assert self.table.get_oid() is not None
        assert self.table.get_id() is not None
        assert self.table.get_type() is not None
        assert self.table.get_json() is not None
        assert self.table.get_name() is not None

    def test_update_build_connection(self):
        self.table.update_build_behavior({'type': 'sync', 'accumulativeConfig': None})


if __name__ == '__main__':
    unittest.main()
