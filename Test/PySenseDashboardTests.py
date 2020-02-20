import unittest
import PySense
import os


class PySenseDashboardTests(unittest.TestCase):

    def setUp(self):
        self.pyClient = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        self.sample_path = 'C:\\PySense\\'
        self.dashboard = self.pyClient.get_dashboards(parentFolder='PySense')[0]

    def test_get_dashboard_export_png(self):
        path = self.sample_path + '\\' + self.dashboard.get_dashboard_id() + '.png'
        assert self.dashboard.get_dashboard_export_png(
            self.sample_path + '\\' + self.dashboard.get_dashboard_id() + '.png',
            includeTitle='true', includeFilters=True, includeDs=False, width=1000) == path
        os.remove(path)

    def test_get_dashboard_export_pdf(self):
        path = self.sample_path + '\\' + self.dashboard.get_dashboard_id() + '.dash'
        assert self.dashboard.get_dashboard_export_pdf(path, 'A4', 'portrait', 'asis',
                                                       includeTitle=True, includeFilters=False, includeDs=True,
                                                       widgetid=None, preview=True, rowCount=None, showTitle=True,
                                                       showFooter=False, title='Hello World', titleSize='medium',
                                                       titlePosition='flex-start') == path

    def test_get_dashboard_dash_export(self):
        path = self.sample_path + '\\' + self.dashboard.get_dashboard_id() + '.dash'
        assert self.dashboard.get_dashboard_export_dash(path) == path

    def test_get_dashboard_widgets(self):
        widget_array = self.dashboard.get_dashboard_widgets()
        assert len(widget_array) == 2
        widget = self.dashboard.get_dashboards_widget_by_id(widget_array[0].get_widget_id())
        assert widget.get_widget_id() == widget_array[0].get_widget_id()


