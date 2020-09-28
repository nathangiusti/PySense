import json
import os
import unittest

from PySense import PySense
from PySense import PySenseDashboard
from PySense import PySenseDataModel
from PySense import SisenseRole


class PySenseTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('//Users//nathan.giusti//Documents//PySense//VmConfig.yaml')
        cls.py_client_linux = PySense.authenticate_by_file(
            '//Users//nathan.giusti//Documents//PySense//PySenseLinux.yaml')
        cls.sample_path = '//Users//nathan.giusti//Documents//PySense//'
        cls.group_names = ["TempGroup", "TempGroup2"]

    def test_get_dashboards(self):
        ret = self.py_client.get_dashboards(name='PySense')
        assert len(ret) == 1
        assert ret[0].get_title() == 'PySense'
        ret = self.py_client.get_dashboards_admin()
        assert len(ret) > 1

    def test_get_dashboards_id(self):
        ret = self.py_client.get_dashboards(name='PySense')
        dashboard_id = ret[0].get_id()
        assert dashboard_id == self.py_client.get_dashboard_by_id(dashboard_id).get_id()

    def test_dashboard_import_delete(self):
        dash = self.py_client.import_dashboard(self.sample_path + 'ImportDash.dash')
        assert dash is not None
        self.py_client.delete_dashboards(dash)
        self.py_client.add_dashboards(dash)

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
        user = self.py_client.add_user('thisisfake@example.com', SisenseRole.Role.from_str('Viewer'), groups=group)
        assert user is not None
        self.py_client.delete_users(user)
        assert len(self.py_client.get_users(user_name='new name')) == 0

    def test_get_elasticubes(self):
        ret = self.py_client.get_elasticubes()
        assert len(ret) > 1
        ret = self.py_client.get_elasticube_by_name('PySense')
        assert ret.get_title() == 'PySense'

    def test_get_add_remove_group(self):
        groups = self.py_client.add_groups(self.group_names)
        assert len(self.py_client.get_groups_by_name(self.group_names)) == len(self.group_names)
        temp_group = self.py_client.get_groups(name="TempGroup2")[0]
        assert temp_group.get_name() == "TempGroup2"
        assert len(groups) == 2
        group_id_arr = []
        for group in groups:
            group_id_arr.append(group.get_id())
        groups = self.py_client.get_groups(ids=group_id_arr)
        assert len(groups) == 2
        self.py_client.delete_groups(groups)

    def test_get_import_export_delete_data_model(self):
        data_model = self.py_client_linux.get_data_models(title='PySense')
        assert isinstance(data_model, PySenseDataModel.DataModel)

        path = data_model.export_to_smodel(self.sample_path + data_model.get_oid() + '.smodel')

        self.py_client_linux.delete_data_model(data_model)
        imported_data_model = self.py_client_linux.import_schema(path)
        assert isinstance(imported_data_model, PySenseDataModel.DataModel)

        data_model = self.py_client_linux.get_data_models(title='PySense')
        assert isinstance(data_model, PySenseDataModel.DataModel)
        os.remove(path)

    def test_branding(self):
        branding = self.py_client_linux.get_branding()
        assert branding is not None
        self.py_client_linux.set_branding(branding)

    def test_roles(self):
        assert self.py_client.get_role_id(SisenseRole.Role.VIEWER) is not None

    @classmethod
    def tearDownClass(cls):
        groups_to_delete = []
        for group in cls.py_client.get_groups():
            if group.get_name() in cls.group_names:
                groups_to_delete.append(group)
        cls.py_client.delete_groups(groups_to_delete)


if __name__ == '__main__':
    unittest.main()
