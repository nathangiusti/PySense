import unittest

from PySense import PySense


class PySenseFormulaTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('C:\\PySense\\VmConfig.yaml')
        cls.elasticube = cls.py_client.get_elasticube_by_name('PySense')
        cls.formula = cls.elasticube.get_saved_formulas()[0]

    def test_getters(self):
        assert self.formula.get_oid() is not None
        assert self.formula.get_json() is not None

    def test_change_datasource(self):
        self.formula.change_datasource(self.elasticube)
        self.elasticube.add_formula_to_cube(self.formula)