import unittest

import PySense.PySense as PySense


class PySenseGroupTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('//Users//nathan.giusti//Documents//PySense//VmConfig.yaml')
        cls.sample_path = 'C:\\PySense\\'
        if len(cls.py_client.get_groups(name='PySense')) == 0:
            cls.py_client.add_groups('PySense')
        cls.group = cls.py_client.get_groups(name='PySense')[0]

    def test_getters(self):
        assert self.group.get_id() is not None
        assert self.group.get_name() is not None
        assert self.group.get_users() is not None

    def test_add_remove_user(self):
        user = self.py_client.get_users(email='nathan.giusti@sisense.com')
        self.group.add_user(user)
        assert len(self.group.get_users()) == 1
        self.group.remove_user(user)
        assert len(self.group.get_users()) == 0


if __name__ == '__main__':
    unittest.main()

