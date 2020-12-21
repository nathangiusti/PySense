import unittest

from PySense import PySense


class PySenseRuleTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('resources//TestConfig.yaml')
        cls.elasticube = cls.py_client.get_elasticube_by_name('PySense')
        cls.user = cls.py_client.get_user_by_email('pysensetest@sisense.com')
        cls.rule = cls.elasticube.add_data_security_rule('Dim_Dates', 'Business Value', 'numeric',
                                                         members=['1'], shares=[cls.user])

    def test_getters(self):
        assert self.rule.get_column() is not None
        assert self.rule.get_id() is not None
        assert self.rule.get_members() is not None
        assert self.rule.get_table() is not None
        assert self.rule.get_shares_json() is not None
        assert self.rule.get_exclusionary() is not None
        assert self.rule.get_shares_user_groups() is not None

    def test_update_rule(self):
        self.rule.update_rule(members=[2, 3])
        assert len(self.rule.get_members()) == 2

    @classmethod
    def tearDownClass(cls):
        cls.elasticube.delete_data_security_rule('Dim_Dates', 'Business Value')
