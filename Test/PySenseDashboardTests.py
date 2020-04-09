import os
import unittest

import PySense.PySense as PySense


class PySenseDashboardTests(unittest.TestCase):

    def setUp(self):
        self.py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        self.sample_path = 'C:\\PySense\\'
        self.dashboard = self.py_client.get_dashboards(parent_folder_name='PySense')[0]

    def test_get_dashboard_export_png(self):
        path = self.sample_path + '\\' + self.dashboard.get_id() + '.png'
        assert self.dashboard.export_to_png(
            path=self.sample_path + '\\' + self.dashboard.get_id() + '.png',
            include_title='true', include_filters=True, include_ds=False, width=1000) == path
        os.remove(path)

    def test_get_dashboard_export_pdf(self):
        path = self.sample_path + '\\' + self.dashboard.get_id() + '.dash'
        assert self.dashboard.export_to_pdf('A4', 'portrait', 'asis', path=path,
                                            include_title=True, include_filters=False, include_ds=True,
                                            widget_id=None, preview=True, row_count=None, show_title=True,
                                            show_footer=False, title='Hello World', title_size='medium',
                                            title_position='flex-start') == path
        os.remove(path)

    def test_get_dashboard_dash_export(self):
        path = self.sample_path + '\\' + self.dashboard.get_id() + '.dash'
        assert self.dashboard.export_to_dash(path=path) == path
        os.remove(path)

    def test_dashboard_widgets(self):
        widget_array = self.dashboard.get_widgets()
        assert len(widget_array) == 2
        widget = self.dashboard.get_widget_by_id(widget_array[0].get_id())
        assert widget.get_id() == widget_array[0].get_id()
        added_widget = self.dashboard.add_widget(widget)
        assert len(self.dashboard.get_widgets()) == 3
        self.dashboard.delete_widget(added_widget.get_id())
        assert len(self.dashboard.get_widgets()) == 2

    def test_dashboard_shares(self):
        shares = self.dashboard.share_to_user('thisistemp@example.com', 'view', 'false')
        assert len(shares['sharesTo']) == 2
        shares = self.dashboard.unshare_to_user('thisistemp@example.com')
        assert len(shares['sharesTo']) == 1

    def test_move_to_folder(self):
        folder = self.py_client.get_folders(name='PySense')[0]
        self.dashboard.move_to_folder(None)
        assert self.dashboard.get_dashboard_folder_id() is None
        self.dashboard.move_to_folder(folder)
        assert self.dashboard.get_dashboard_folder_id() == folder.get_folder_id()

    def test_remove_ghost_widgets(self):
        self.dashboard.remove_ghost_widgets()






