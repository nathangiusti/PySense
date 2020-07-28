import unittest

from PySense import PySense


class PySenseUserTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        cls.user = cls.py_client.get_user_by_email('testuser@sisense.com')
        if cls.user is None:
            cls.user = cls.py_client.add_user('testuser@sisense.com', 'Viewer', first_name='Test', last_name='User')
        cls.group = cls.py_client.get_groups(name='PySense')[0]

    def test_getters(self):
        assert self.user.get_id() is not None
        assert self.user.get_user_name() is not None
        assert self.user.get_email() is not None
        assert self.user.get_first_name() is not None
        assert self.user.get_last_name() is not None
        assert self.user.get_role() is not None

    def test_update_user(self):
        self.user.update(first_name='Nathan', last_name='Giusti', groups=self.group)
        assert self.user.get_first_name() == 'Nathan'
        assert self.user.get_last_name() == 'Giusti'
        assert len(self.user.get_groups()) == 1
        assert self.user.get_groups()[0].get_name() == self.group.get_name()
        self.user.update(first_name='PySense', last_name='User', groups=[])
        assert self.user.get_first_name() == 'PySense'
        assert self.user.get_last_name() == 'User'
        assert len(self.user.get_groups()) == 0
