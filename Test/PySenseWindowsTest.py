import unittest

from PySense import PySense


class PySenseWindowsTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('resources//WindowsConfig.yaml')
        cls.elasticube = cls.py_client.get_elasticube_by_name('PySense')

    def test_cube_build_start_stop(self):
        self.elasticube.stop_cube()
        self.elasticube.start_cube()
        self.elasticube.restart_cube()
        self.elasticube.start_build('delta')
        self.elasticube.stop_build()

