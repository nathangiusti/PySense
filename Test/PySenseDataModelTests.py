import os
import unittest

from PySense import PySense


class PySenseDataModelTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('resources//LinuxConfig.yaml')
        cls.data_model = cls.py_client.get_data_models(title='PySense')[0]
        cls.tmp = 'tmp//'
        cls.resources = 'resources//'

    def test_getters(self):
        assert self.data_model.get_title() == 'PySense'
        assert self.data_model.get_oid() is not None
        temp = self.data_model.get_creator()
        assert self.data_model.get_creator() is not None

    def test_export_import(self):
        new_data_model = self.py_client.import_schema(self.resources + 'AnotherModel.smodel')
        assert new_data_model is not None
        new_data_model = self.py_client.import_schema(self.resources + 'AnotherModel.smodel',
                                                  target_data_model_id=new_data_model.get_oid())
        path = new_data_model.export_to_smodel(self.tmp + 'Temp.smodel')
        os.remove(path)
        path = new_data_model.export_to_sdata(self.tmp + 'Temp.sdata')
        # This method often fails due to API limitations
        # new_data_model = self.py_client.import_sdata(self.tmp + 'Temp.sdata', target_data_model_id=self.data_model.get_oid())
        os.remove(path)

        self.py_client.delete_data_models(new_data_model)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.tmp + 'Temp.smodel'):
            os.remove(cls.tmp + 'Temp.smodel')
        if os.path.exists(cls.tmp + 'Temp.sdata'):
            os.remove(cls.tmp + 'Temp.sdata')


""" The REST API is consistently unreliable surround the build status check so I have disabled this test
    def test_build_cancel(self):
        build = self.data_model.start_build('full')
        time.sleep(1)
        while build.get_status() is None:
            time.sleep(1)
        build.cancel_build()
"""


if __name__ == '__main__':
    unittest.main()
