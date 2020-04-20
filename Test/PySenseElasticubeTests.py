import unittest

import PySense.PySense as PySense
import PySense.PySenseException as PySenseException


class PySenseElasticubeTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        cls.elasticube = cls.py_client.get_elasticube_by_name('PySense')

    def test_get_model(self):
        model = self.elasticube.get_model()
        assert model is not None

    def test_get_add_modify_delete_security_rule(self):
        default_rule = self.elasticube.add_default_rule('Dim_Dates', 'BusinessDay', 'numeric')
        assert default_rule is not None
        
        shares = self.py_client.get_users(email='testuser@sisense.com')
        shares.extend(self.py_client.get_groups(name='PySense'))
        
        rule = self.elasticube.add_security_rule(shares, 'Dim_Dates', 'BusinessDay', 'numeric', members=["1"])
        assert len(self.elasticube.get_security_for_user(shares[0])) == 2
        assert len(self.elasticube.get_datasecurity()) == 2
        assert len(self.elasticube.
                   get_datasecurity_by_table_column('Dim_Dates', 'BusinessDay')) == 2
        rule.update_rule(shares=shares, table='Dim_Dates', column='BusinessDay', 
                         data_type='numeric', members=[0])
        assert rule.get_members()[0] == '0'
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

    @classmethod
    def tearDownClass(cls):
        try: 
            cls.elasticube.delete_rule('Dim_Dates', 'BusinessDay')
        except PySenseException.PySenseException:
            None
        
        
if __name__ == '__main__':
    unittest.main()
