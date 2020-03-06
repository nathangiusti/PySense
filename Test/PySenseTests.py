import json
import os
import unittest

from PySense import PySense


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
            data = json.loads(file.read())
        dash = self.pyClient.post_dashboards(data)
        assert dash is not None
        assert self.pyClient.delete_dashboards(dash.get_dashboard_id()) is not None

    def test_get_folders(self):
        temp = self.pyClient.get_folders(name='PySense')
        assert len(temp) == 1
        assert temp[0].get_folder_name() == 'PySense'

    def test_get_folder_by_name_by_id(self):
        folder = self.pyClient.get_folders(name='PySense')[0]
        assert folder.get_folder_name() == 'PySense'
        folder2 = self.pyClient.get_folders_id(folder.get_folder_id())
        assert folder.get_folder_id() == folder2.get_folder_id()

    def test_post_update_delete_user(self):
        user = self.pyClient.post_user('thisisfake@example.com', 'fake', 'Viewer', groups=['PySense'])
        assert user is not None
        user.update_user(user_name='new name')
        assert user.get_user_user_name() == 'new name'
        self.pyClient.delete_user(user)
        assert len(self.pyClient.get_users(user_name='new name')) == 0

    def test_custom_rest(self):
        resp = self.pyClient.custom_rest('get', 'api/v1/plugins')
        assert resp.status_code in [200, 201, 204]

    def test_get_elasticubes(self):
        ret = self.pyClient.get_elasticubes()
        assert len(ret) > 1
        ret = self.pyClient.get_elasticube_by_name('PySense')
        assert ret.get_name() == 'PySense'

    def test_get_add_remove_group(self):
        group_names = ["TempGroup", "TempGroup2"]
        groups = self.pyClient.add_groups(group_names)
        temp_group = self.pyClient.get_groups(name="TempGroup2")[0]
        assert temp_group.get_group_name() == "TempGroup2"
        assert len(groups) == 2
        group_id_arr = []
        for group in groups:
            group_id_arr.append(group.get_group_id())
        groups = self.pyClient.get_groups(ids=group_id_arr)
        assert len(groups) == 2
        assert self.pyClient.delete_groups(groups) is True


if __name__ == '__main__':
    unittest.main()
