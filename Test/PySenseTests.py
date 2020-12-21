import unittest

from PySense import PySense, SisenseRole


class PySenseTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('resources//TestConfig.yaml')
        cls.resources = 'resources//'
        cls.tmp = 'tmp//'

    def test_params(self):
        cube_timeout = self.py_client.get_param('CUBE_CACHE_TIMEOUT_SECONDS')
        assert cube_timeout == 60
        self.py_client.set_param('new_param', 'new value')
        assert self.py_client.get_param('new_param') == 'new value'

    def test_get_dashboards(self):
        ret = self.py_client.get_dashboards(name='PySense')
        assert len(ret) == 1
        assert ret[0].get_title() == 'PySense'
        ret = self.py_client.get_dashboards_admin()
        assert len(ret) > 1

    def test_get_dashboards_id(self):
        ret = self.py_client.get_dashboards(name='PySense')
        dashboard_id = ret[0].get_oid()
        assert dashboard_id == self.py_client.get_dashboard_by_id(dashboard_id).get_oid()

    def test_dashboard_import_delete(self):
        dash = self.py_client.import_dashboards(self.resources + 'AnotherDash.dash')
        assert dash is not None
        self.py_client.delete_dashboards(dash)
        dash = self.py_client.add_dashboards(dash)
        self.py_client.delete_dashboards(dash)

    def test_create_dashboard(self):
        dashboard = self.py_client.create_dashboard('Test Dashboard')
        self.py_client.delete_dashboards(dashboard)

    def test_get_folders(self):
        temp = self.py_client.get_folders(name='PySense')
        assert len(temp) == 1
        assert temp[0].get_name() == 'PySense'

    def test_get_folder_by_name_by_id(self):
        folder = self.py_client.get_folders(name='PySense')[0]
        assert folder.get_name() == 'PySense'
        folder2 = self.py_client.get_folder_by_id(folder.get_oid())
        assert folder.get_oid() == folder2.get_oid()

    def test_post_update_delete_user(self):
        group = self.py_client.get_groups(name='PySense')
        user = self.py_client.add_user('thisisfake@example.com', SisenseRole.Role.from_str('Viewer'),
                                       user_name='thisisafakeusername', groups=group)
        assert user is not None
        self.py_client.delete_users(user)
        assert len(self.py_client.get_users(user_name='thisisafakeusername')) == 0

    def test_get_elasticubes(self):
        ret = self.py_client.get_elasticubes()
        assert len(ret) > 1
        ret = self.py_client.get_elasticube_by_name('PySense')
        assert ret.get_title() == 'PySense'

    def test_branding(self):
        branding = self.py_client.get_branding()
        assert branding is not None
        self.py_client.set_branding(branding)

    def test_ui_settings(self):
        settings = self.py_client.get_ui_settings()[0]
        assert settings is not None
        self.py_client.set_ui_settings(settings)

    def test_roles(self):
        assert self.py_client.get_role_id(SisenseRole.Role.VIEWER) is not None


if __name__ == '__main__':
    unittest.main()
