import unittest

from PySense import PySense


class PySenseTableTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('C:\\PySense\\VmConfig.yaml')
        cls.table = cls.py_client.get_elasticube_by_name('PySense').get_model().get_data_sets()[0].get_tables()[0]

    def test_getters(self):
        assert self.table.get_config_option('ApiVersion') is not None
        options = self.table.get_config_options()
        assert options is not None
        assert options['ApiVersion'] == self.table.get_config_option('ApiVersion')


if __name__ == '__main__':
    unittest.main()
