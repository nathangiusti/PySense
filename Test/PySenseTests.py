import json
import os
import unittest
import PySense

sample_dash_id = None
sample_path = 'C:\\PySenseTests'


class PySenseTests(unittest.TestCase):
    pyClient = None
    @classmethod
    def setUp(cls):
        cls.pyClient = PySense.authenticate_by_file('C:\\PySenseConfig.yaml')

    def test_auth(self):
        assert self.pyClient.get_authentication() is not None

    def test_get_folders(self):
        temp = self.pyClient.get_folders(name='PySense')
        assert len(temp) == 1
        assert temp[0]['name'] == 'PySense'

    def test_get_dashboards(self):
        ret = self.pyClient.get_dashboards(parentFolder='PySense')
        assert len(ret) == 1
        assert ret[0].get_dashboard_title() == 'PySense'

    def test_get_folder_by_name(self):
        assert self.pyClient.get_folders(name='PySense')[0]['name'] == 'PySense'

    def test_get_dashboard_export_png(self):
        ret = self.pyClient.get_dashboards(parentFolder='PySense')[0]
        path = sample_path + '\\' + ret.get_dashboard_id() + '.png'
        assert path == ret.get_dashboard_export_png(sample_path + '\\' + ret.get_dashboard_id() + '.png',
                                         includeTitle='true', includeFilters=True, includeDs=False, width=1000)
        os.remove(path)

    def test_dashboard_dash_export(self):
        dash = self.pyClient.get_dashboards(parentFolder='PySense')[0]
        path = sample_path + '\\' + dash.get_dashboard_id() + '.dash'
        assert dash.get_dashboard_export_dash(path) == path

    def test_dashboard_import_delete(self):
        with open(sample_path + '\\' + 'ImportDash.dash', 'r', encoding="utf8") as file:
            data = file.read()
        dash = self.pyClient.post_dashboards(data)
        assert dash is not None
        assert self.pyClient.delete_dashboards(dash.get_dashboard_id()) is not None


if __name__ == '__main__':
    unittest.main()
