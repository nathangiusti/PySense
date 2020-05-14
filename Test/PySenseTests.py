import json
import unittest

from PySense import PySense
from PySense import PySenseDataModel
from PySense import PySenseException


class PySenseTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        cls.py_client_linux = PySense.authenticate_by_file('C:\\PySense\\PySenseLinux.yaml')
        cls.sample_path = 'C:\\PySense\\'
        cls.group_names = ["TempGroup", "TempGroup2"]

    def test_get_dashboards(self):
        ret = self.py_client.get_dashboards(name='PySense')
        assert len(ret) == 1
        assert ret[0].get_name() == 'PySense'

    def test_get_dashboards_id(self):
        ret = self.py_client.get_dashboards(name='PySense')
        dashboard_id = ret[0].get_id()
        assert dashboard_id == self.py_client.get_dashboard_by_id(dashboard_id).get_id()

    def test_dashboard_import_delete(self):
        with open(self.sample_path + '\\' + 'ImportDash.dash', 'r', encoding="utf8") as file:
            data = json.loads(file.read())
        dash = self.py_client.post_dashboards(data)
        assert dash is not None
        self.py_client.delete_dashboards(dash)

    def test_get_folders(self):
        temp = self.py_client.get_folders(name='PySense')
        assert len(temp) == 1
        assert temp[0].get_name() == 'PySense'

    def test_get_folder_by_name_by_id(self):
        folder = self.py_client.get_folders(name='PySense')[0]
        assert folder.get_name() == 'PySense'
        folder2 = self.py_client.get_folder_by_id(folder.get_id())
        assert folder.get_id() == folder2.get_id()

    def test_post_update_delete_user(self):
        group = self.py_client.get_groups(name='PySense')
        user = self.py_client.add_user('thisisfake@example.com', 'Viewer', groups=group)
        assert user is not None
        self.py_client.delete_users(user)
        assert len(self.py_client.get_users(user_name='new name')) == 0

    def test_get_elasticubes(self):
        ret = self.py_client.get_elasticubes()
        assert len(ret) > 1
        ret = self.py_client.get_elasticube_by_name('PySense')
        assert ret.get_name() == 'PySense'

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
        
        self.py_client_linux.delete_data_model(data_model)
        with self.assertRaises(PySenseException.PySenseException):
            data_model = self.py_client_linux.get_data_models(title='PySense')
        
        self.py_client_linux.add_data_model(data_model)
        data_model = self.py_client_linux.get_data_models(title='PySense')
        assert isinstance(data_model, PySenseDataModel.DataModel)
    
    @classmethod
    def tearDownClass(cls):
        groups_to_delete = []
        for group in cls.py_client.get_groups():
            if group.get_name() in cls.group_names:
                groups_to_delete.append(group)
        cls.py_client.delete_groups(groups_to_delete)
                
                
if __name__ == '__main__':
    unittest.main()
