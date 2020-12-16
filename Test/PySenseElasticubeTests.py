import os
import unittest

import PySense.PySense as PySense
import PySense.PySenseException as PySenseException


class PySenseElasticubeTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('resources//WindowsConfig.yaml')
        cls.elasticube = cls.py_client.get_elasticube_by_name('PySense')
        cls.linux_client = PySense.authenticate_by_file('resources//LinuxConfig.yaml')
        cls.linux_elasticube = cls.linux_client.get_elasticube_by_name('PySense')
        cls.tmp = 'tmp//'

    def test_getters(self):
        assert self.elasticube.get_title() is not None

    def test_shares(self):
        shares = self.py_client.get_users(email='pysensetest@sisense.com')
        group_share = self.py_client.get_groups(name='PySense')
        self.elasticube.add_share(shares)
        self.elasticube.add_share(group_share)
        assert len(self.elasticube.get_shares_user_group()) == 3
        assert len(self.elasticube.get_shares_json()) == 3
        self.elasticube.remove_shares(shares)
        self.elasticube.remove_shares(group_share)
        assert len(self.elasticube.get_shares_json()) == 1
        assert len(self.elasticube.get_shares_user_group()) == 1

    def test_get_add_modify_delete_security_rule(self):
        default_rule = self.elasticube.add_data_security_rule('Dim_Dates', 'BusinessDay', 'numeric', members=['1'])
        assert default_rule is not None
        assert default_rule.get_members() == ['1']

        with self.assertRaises(PySense.PySenseException.PySenseException):
            self.elasticube.add_data_security_rule('Dim_Dates', 'BusinessDay', 'numeric', shares=['Some user'])

        shares = self.py_client.get_users(email='pysensetest2@sisense.com')
        shares.extend(self.py_client.get_groups(name='PySense'))

        rule = self.elasticube.add_data_security_rule('Dim_Dates', 'BusinessDay', 'numeric', shares=shares, members=["1"])

        # This end point does not seem to work. Tested on swagger and it does not pull correct results
        # The rule is there, but this endpoint does not pull them. Always returns empty
        # assert len(self.elasticube.get_datasecurity_for_user(shares[0])) == 2
        assert len(self.elasticube.get_data_security()) == 2
        assert len(self.elasticube.
                   get_data_security_by_table_column('Dim_Dates', 'BusinessDay')) == 2
        rule.update_rule(shares=shares, table='Dim_Dates', column='BusinessDay',
                         data_type='numeric', members=[0])
        assert rule.get_members()[0] == '0'
        self.elasticube.delete_data_security_rule('Dim_Dates', 'BusinessDay')
        assert len(self.elasticube.
                   get_data_security_by_table_column('Dim_Dates', 'BusinessDay')) == 0

    def test_cube_build_start_stop(self):
        self.elasticube.stop_cube()
        self.elasticube.start_cube()
        self.elasticube.restart_cube()
        self.elasticube.start_build('delta')
        self.elasticube.stop_build()

    def test_run_sql(self):
        path = self.elasticube.run_sql("SELECT * FROM Dim_Dates", 'csv', self.tmp + 'file.csv')
        os.remove(path)
        path = self.linux_elasticube.run_sql("SELECT * FROM Dim_Dates", 'csv', self.tmp + 'file.csv')
        os.remove(path)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.elasticube.delete_data_security_rule('Dim_Dates', 'BusinessDay')
        except PySenseException.PySenseException:
            None


if __name__ == '__main__':
    unittest.main()
