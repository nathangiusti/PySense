import unittest

import PySense.PySense as PySense


class PySenseGroupTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        cls.sample_path = 'C:\\PySense\\'
        cls.group = cls.py_client.get_groups(name='PySense')[0]
        
    def test_getters(self):
        assert self.group.get_id() is not None
        assert self.group.get_name() is not None
        assert self.group.get_users() is not None

    def test_add_remove_user(self):
        user = self.py_client.get_users(email='testuser@sisense.com')
        self.group.add_user(user)
        assert len(self.group.get_users()) == 2
        self.group.remove_user(user)
        assert len(self.group.get_users()) == 1
      
        
if __name__ == '__main__':
    unittest.main()

