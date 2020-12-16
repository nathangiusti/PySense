import unittest

from PySense import PySense, SisenseRole


class PySenseUserTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('resources//WindowsConfig.yaml')
        cls.user = cls.py_client.get_user_by_email('pysensetest@sisense.com')
        cls.group = cls.py_client.get_groups(name='PySense')[0]

    def test_getters(self):
        assert self.user.get_id() is not None
        assert self.user.get_user_name() is not None
        assert self.user.get_email() is not None
        assert self.user.get_first_name() is not None
        assert self.user.get_last_name() is not None
        assert self.user.get_role() == SisenseRole.Role.DESIGNER

    def test_update_user(self):
        self.user.update(first_name='PySense', last_name='User', groups=[])
        assert self.user.get_first_name() == 'PySense'
        assert self.user.get_last_name() == 'User'
        assert len(self.user.get_groups()) == 0
