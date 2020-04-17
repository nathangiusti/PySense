import unittest

from PySense import PySense


class PySenseRuleTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        cls.elasticube = cls.py_client.get_elasticube_by_name('PySense')
        cls.user = cls.py_client.get_user_by_email('testuser@sisense.com')
        cls.rule = cls.elasticube.add_security_rule(cls.user, 'Dim_Dates', 'BusinessValue', 'numeric', members=[1])
        
    def test_getters(self):
        assert self.rule.get_column() is not None
        assert self.rule.get_id() is not None
        assert self.rule.get_members() is not None
        assert self.rule.get_table() is not None
        assert self.rule.get_shares() is not None
        assert self.rule.get_exclusionary() is not None
        
    def test_update_rule(self):
        self.rule.update_rule(members=[2, 3])
        assert len(self.rule.get_members()) == 2

    @classmethod
    def tearDownClass(cls):
        cls.elasticube.delete_rule('Dim_Dates', 'BusinessValue')
