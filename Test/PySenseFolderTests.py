import unittest

from PySense import PySense


class PySenseFolderTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('resources//TestConfig.yaml')
        cls.folder = cls.py_client.get_folders(name='PySense')[0]

    def test_getters(self):
        assert self.folder.get_name() is not None
        assert self.folder.get_oid() is not None

