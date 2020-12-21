import unittest
import os

from PySense import PySense, PySenseDataModel


class PySenseLinuxTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('resources//LinuxConfig.yaml')
        cls.elasticube = cls.py_client.get_elasticube_by_name('PySense')
        cls.tmp = 'tmp//'

    def test_get_data_model(self):
        assert self.elasticube.get_data_model() is not None
