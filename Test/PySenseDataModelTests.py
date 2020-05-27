import time
import unittest

from PySense import PySense


class PySenseDataModelTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseLinux.yaml')
        cls.data_model = cls.py_client.get_data_models(title='PySense')

    def test_getters(self):
        assert self.data_model.get_title() == 'PySense'
        assert self.data_model.get_oid() is not None
        assert self.data_model.get_schema_json() is not None
        assert self.data_model.get_json() is not None

    def test_build_cancel(self):
        build = self.data_model.start_build('full')
        time.sleep(1)
        while build.get_status() is None:
            time.sleep(1)
        print(build.get_status())
        time.sleep(1)
        build.cancel_build()


if __name__ == '__main__':
    unittest.main()
