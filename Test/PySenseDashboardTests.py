import os
import unittest

import PySense.PySense as PySense


class PySenseDashboardTests(unittest.TestCase):

    def setUp(self):
        self.pyClient = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        self.sample_path = 'C:\\PySense\\'
        self.dashboard = self.pyClient.get_dashboards(parent_folder_name='PySense')[0]

    def test_get_dashboard_export_png(self):
        path = self.sample_path + '\\' + self.dashboard.get_dashboard_id() + '.png'
        assert self.dashboard.get_dashboard_export_png(
            self.sample_path + '\\' + self.dashboard.get_dashboard_id() + '.png',
            include_title='true', include_filters=True, include_ds=False, width=1000) == path
        os.remove(path)

    def test_get_dashboard_export_pdf(self):
        path = self.sample_path + '\\' + self.dashboard.get_dashboard_id() + '.dash'
        assert self.dashboard.get_dashboard_export_pdf(path, 'A4', 'portrait', 'asis',
                                                       include_title=True, include_filters=False, include_ds=True,
                                                       widget_id=None, preview=True, row_count=None, show_title=True,
                                                       show_footer=False, title='Hello World', title_size='medium',
                                                       title_position='flex-start') == path

    def test_get_dashboard_dash_export(self):
        path = self.sample_path + '\\' + self.dashboard.get_dashboard_id() + '.dash'
        assert self.dashboard.get_dashboard_export_dash(path) == path

    def test_dashboard_widgets(self):
        widget_array = self.dashboard.get_dashboard_widgets()
        assert len(widget_array) == 2
        widget = self.dashboard.get_dashboards_widget_by_id(widget_array[0].get_widget_id())
        assert widget.get_widget_id() == widget_array[0].get_widget_id()
        added_widget = self.dashboard.post_dashboards_widgets(widget)
        assert len(self.dashboard.get_dashboard_widgets()) == 3
        self.dashboard.delete_dashboards_widgets(added_widget.get_widget_id())
        assert len(self.dashboard.get_dashboard_widgets()) == 2

    def test_dashboard_shares(self):
        shares = self.dashboard.share_dashboard_to_user('thisistemp@example.com', 'view', 'false')
        assert len(shares['sharesTo']) == 2
        shares = self.dashboard.unshare_dashboard_to_user('thisistemp@example.com')
        assert len(shares['sharesTo']) == 1

    def test_move_to_folder(self):
        folder = self.pyClient.get_folders(name='PySense')[0]
        self.dashboard.move_to_folder(None)
        assert self.dashboard.get_dashboard_folder_id() is None
        self.dashboard.move_to_folder(folder)
        assert self.dashboard.get_dashboard_folder_id() == folder.get_folder_id()

    def test_remove_ghost_widgets(self):
        self.dashboard.remove_ghost_widgets()






