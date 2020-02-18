import unittest
import PySense
import os


class PySenseDashboardTests(unittest.TestCase):

    def setUp(cls):
        cls.pyClient = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        cls.sample_path = 'C:\\PySense\\'

    def test_get_dashboard_export_png(self):
        ret = self.pyClient.get_dashboards(parentFolder='PySense')[0]
        path = self.sample_path + '\\' + ret.get_dashboard_id() + '.png'
        assert path == ret.get_dashboard_export_png(self.sample_path + '\\' + ret.get_dashboard_id() + '.png',
                                                    includeTitle='true', includeFilters=True, includeDs=False,
                                                    width=1000)
        os.remove(path)

    def test_dashboard_dash_export(self):
        dash = self.pyClient.get_dashboards(parentFolder='PySense')[0]
        path = self.sample_path + '\\' + dash.get_dashboard_id() + '.dash'
        assert dash.get_dashboard_export_dash(path) == path

