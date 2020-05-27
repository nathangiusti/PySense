import unittest

from PySense import PySense


class PySenseDataSetTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        cls.data_set = cls.py_client.get_elasticube_by_name('PySense').get_model().get_data_sets()[0]

    def test_getters(self):
        assert self.data_set.get_source() is not None
        assert self.data_set.get_oid() is not None
        assert self.data_set.get_full_name() is not None
        assert self.data_set.get_tables() is not None
        assert self.data_set.get_type() is not None


if __name__ == '__main__':
    unittest.main()
