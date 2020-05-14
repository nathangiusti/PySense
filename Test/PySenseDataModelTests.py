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
        
        
if __name__ == '__main__':
    unittest.main()
