import unittest

import PySense.PySense as PySense


class PySenseElasticubeTests(unittest.TestCase):
    
    def setUp(self):
        self.py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        self.elasticube = self.py_client.get_elasticube_by_name('PySense')

    def test_get_model(self):
        model = self.elasticube.get_model()
        assert model is not None

    def test_get_add_modify_delete_security_rule(self):
        user = self.py_client.get_users(email='nathan.giusti@sisense.com')[0]
        group = self.py_client.get_groups(name='PySense')[0]
        default_rule = self.elasticube.add_default_rule('Dim_Dates', 'BusinessDay', 'numeric')
        assert default_rule is not None
        rule = self.elasticube.add_security_rule([user, group], 'Dim_Dates', 'BusinessDay', 'numeric', [1],
                                                 exclusionary=True, all_members=False)
        assert len(self.elasticube.get_security_for_user(user)) == 2
        assert len(self.elasticube.get_datasecurity()) == 2
        assert len(self.elasticube.
                   get_datasecurity_by_table_column('Dim_Dates', 'BusinessDay')) == 2
        rule.update_rule([user, group], 'Dim_Dates', 'BusinessDay', 'numeric', [0])
        assert rule.get_member_values()[0] == '0'
        self.elasticube.delete_rule('Dim_Dates', 'BusinessDay')
        assert len(self.elasticube.
                   get_datasecurity_by_table_column('Dim_Dates', 'BusinessDay')) == 0

    def test_formulas(self):
        formulas = self.elasticube.get_saved_formulas()
        formula_len = len(formulas)
        formula = formulas[0]
        self.elasticube.delete_formulas([formula])
        formula.change_datasource(self.elasticube)
        self.elasticube.add_formula_to_cube(formula)
        assert formula_len == len(self.elasticube.get_saved_formulas())
        
        
if __name__ == '__main__':
    unittest.main()
