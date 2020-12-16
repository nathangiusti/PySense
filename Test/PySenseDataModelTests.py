import os
import unittest

from PySense import PySense


class PySenseDataModelTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('resources//LinuxConfig.yaml')
        cls.data_model = cls.py_client.get_data_models(title='PySense')[0]
        cls.dir = 'tmp//'

    def test_getters(self):
        assert self.data_model.get_title() == 'PySense'
        assert self.data_model.get_oid() is not None

    def test_export_import(self):
        self.data_model.export_to_smodel(self.dir + 'Temp.smodel')
        assert self.py_client.import_schema(self.dir + 'Temp.smodel',
                                            target_data_model=self.data_model) is not None
        os.remove(self.dir + 'Temp.smodel')

        self.data_model.export_to_sdata(self.dir + 'Temp.sdata')

        # This method often fails due to API limitations
        assert self.py_client.import_sdata(self.dir + 'Temp.sdata',
                                           target_data_model=self.data_model) is not None
        os.remove(self.dir + 'Temp.sdata')

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.dir + 'Temp.smodel'):
            os.remove(cls.dir + 'Temp.smodel')
        if os.path.exists(cls.dir + 'Temp.sdata'):
            os.remove(cls.dir + 'Temp.sdata')


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
