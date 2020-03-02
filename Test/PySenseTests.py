import json
import os
import unittest

from PySense import PySense
from PySense import PySenseDashboard


class PySenseTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.pyClient = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        cls.sample_path = 'C:\\PySense\\'

    def test_auth(self):
        assert self.pyClient.get_authentication() is not None

    def test_get_dashboards(self):
        ret = self.pyClient.get_dashboards(parent_folder_name='PySense')
        assert len(ret) == 1
        assert ret[0].get_dashboard_title() == 'PySense'

    def test_get_dashboards_id(self):
        ret = self.pyClient.get_dashboards(parent_folder_name='PySense')
        dashboard_id = ret[0].get_dashboard_id()
        assert dashboard_id == self.pyClient.get_dashboards_id(dashboard_id).get_dashboard_id()

    def test_dashboard_import_delete(self):
        with open(self.sample_path + '\\' + 'ImportDash.dash', 'r', encoding="utf8") as file:
            data = file.read()
        dash = self.pyClient.post_dashboards(PySenseDashboard.Dashboard(self.pyClient.get_authentication()['host'],
                                                                        self.pyClient.get_authentication()['token'],
                                                                        json.loads(data)))
        assert dash is not None
        assert self.pyClient.delete_dashboards(dash.get_dashboard_id()) is not None

    def test_get_folders(self):
        temp = self.pyClient.get_folders(name='PySense')
        assert len(temp) == 1
        assert temp[0].get_folder_name() == 'PySense'

    def test_get_folder_by_name_by_id(self):
        folder = self.pyClient.get_folders(name='PySense')[0]
        assert folder.get_folder_name() == 'PySense'
        folder2 = self.pyClient.get_folders_id(folder.get_folder_oid())
        assert folder.get_folder_oid() == folder2.get_folder_oid()

    def test_post_update_delete_user(self):
        user = self.pyClient.post_user('thisisfake@example.com', 'fake', 'Viewer', groups=['PySense'])
        assert user is not None
        user.update_user(user_name='new name')
        assert user.get_user_user_name() == 'new name'
        self.pyClient.delete_user(user)
        assert len(self.pyClient.get_users(user_name='new name')) == 0

    def test_custom_rest(self):
        resp = self.pyClient.custom_rest('get', 'api/v1/plugins')
        assert resp.response.status_code in [200, 201, 204]

    def test_get_csv_for_table(self):
        path = self.pyClient.get_csv_for_table('Test', self.sample_path + 'test.csv', table_name='DIM_Date')
        assert path == self.sample_path + 'test.csv'
        os.remove(path)


if __name__ == '__main__':
    unittest.main()
