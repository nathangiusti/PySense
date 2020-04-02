import unittest

import PySense.PySense as PySense


class PySenseElasticubeTests(unittest.TestCase):
    def setUp(self):
        self.pyClient = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        self.elasticube = self.pyClient.get_elasticube_by_name('PySense')

    def test_get_model(self):
        model = self.elasticube.get_model()
        assert model is not None

    def test_get_add_modify_delete_security_rule(self):
        user = self.pyClient.get_users(email='nathan.giusti@sisense.com')[0]
        group = self.pyClient.get_groups(name='PySense')[0]
        default_rule = self.elasticube.add_default_rule('LocalHost', 'Dim_Dates', 'BusinessDay', 'numeric')
        assert default_rule is not None
        rule = self.elasticube.add_security_rule('LocalHost', [user, group], 'Dim_Dates', 'BusinessDay', 'numeric', [1],
                                                 exclusionary=True, all_members=False)
        assert len(self.elasticube.get_elasticube_datasecurity('LocalHost')) == 2
        assert len(self.elasticube.
                   get_elasticube_datasecurity_by_table_column('LocalHost', 'Dim_Dates', 'BusinessDay')) == 2
        rule.update_rule([user, group], 'Dim_Dates', 'BusinessDay', 'numeric', [0])
        assert rule.get_member_values()[0] == '0'
        self.elasticube.delete_rule('LocalHost', 'Dim_Dates', 'BusinessDay')
        assert len(self.elasticube.
                   get_elasticube_datasecurity_by_table_column('LocalHost', 'Dim_Dates', 'BusinessDay')) == 0


if __name__ == '__main__':
    unittest.main()
