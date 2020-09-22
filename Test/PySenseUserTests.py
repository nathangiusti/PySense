import unittest

from PySense import PySense
from PySense import SisenseRole


class PySenseUserTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('//Users//nathan.giusti//Documents//PySense//VmConfig.yaml')
        cls.user = cls.py_client.get_user_by_email('testuser@sisense.com')
        if cls.user is None:
            cls.user = cls.py_client.add_user('testuser@sisense.com', SisenseRole.Role.VIEWER,
                                              first_name='Test', last_name='User')
        cls.group = cls.py_client.get_groups(name='PySense')[0]

    def test_getters(self):
        assert self.user.get_id() is not None
        assert self.user.get_user_name() is not None
        assert self.user.get_email() is not None
        assert self.user.get_first_name() is not None
        assert self.user.get_last_name() is not None
        assert self.user.get_role() == SisenseRole.Role.VIEWER

    def test_update_user(self):
        self.user.update(first_name='PySense', last_name='User', groups=[])
        assert self.user.get_first_name() == 'PySense'
        assert self.user.get_last_name() == 'User'
        assert len(self.user.get_groups()) == 0
