import unittest

from PySense import PySense


class PySenseTableTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('resources//LinuxConfig.yaml')
        cls.table = cls.py_client.get_data_models(title='PySense')[0].get_data_sets(source='CSV')[0].get_tables()[0]

    def test_getters(self):
        self.table.get_config_option('hasHeader')
        options = self.table.get_config_options()
        assert options is not None
        assert self.table.get_oid() is not None
        assert self.table.get_oid() is not None
        assert self.table.get_type() is not None
        assert self.table.get_json() is not None
        assert self.table.get_name() is not None

    def test_update_build_connection(self):
        self.table.update_build_behavior({'type': 'sync', 'accumulativeConfig': None})


if __name__ == '__main__':
    unittest.main()
