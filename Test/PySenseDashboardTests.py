import os
import unittest

import PySense.PySense as PySense


class PySenseDashboardTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('//Users//nathan.giusti//Documents//PySense//VmConfig.yaml')
        cls.sample_path = '//Users//nathan.giusti//Documents//PySense//'
        cls.dashboard = cls.py_client.get_dashboards(name='PySense')[0]

    def test_getters(self):
        assert self.dashboard.get_title() is not None
        assert self.dashboard.get_datasource().get_title() == 'PySense'

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
        assert len(widget_array) == 1
        widget = self.dashboard.get_widget_by_id(widget_array[0].get_oid())
        assert widget.get_oid() == widget_array[0].get_oid()
        added_widget = self.dashboard.add_widget(widget)
        assert len(self.dashboard.get_widgets()) == 2
        self.dashboard.delete_widget(added_widget)
        assert len(self.dashboard.get_widgets()) == 1

    def test_dashboard_shares(self):
        user = self.py_client.get_users(email='testuser@sisense.com')[0]
        group = self.py_client.get_groups(name='PySense')[0]
        self.dashboard.add_share([user, group], 'view', 'false')
        assert len(self.dashboard.get_share_users_groups()) == 3
        assert len(self.dashboard.get_shares()['sharesTo']) == 3
        self.dashboard.remove_shares([user, group])
        self.dashboard.get_datasource().remove_shares([user, group])
        assert len(self.dashboard.get_datasource().get_shares()['shares']) == 1
        assert len(self.dashboard.get_shares()['sharesTo']) == 1

    def test_move_to_folder(self):
        folder = self.py_client.get_folders(name='PySense')[0]
        self.dashboard.move_to_folder(None)
        assert self.dashboard.get_folder() is None
        self.dashboard.move_to_folder(folder)
        assert self.dashboard.get_folder().get_oid() == folder.get_oid()

    def test_remove_ghost_widgets(self):
        self.dashboard.remove_ghost_widgets()

    def test_publish(self):
        self.dashboard.publish()

    def test_bulk_export_import(self):
        path = self.sample_path + 'bulkExport.dash'
        folder = self.py_client.get_folders(name='PySense')[0]
        dashboards = self.py_client.get_dashboards(parent_folder=folder)
        self.py_client.bulk_export_dashboards(dashboards, path=path)
        self.py_client.import_dashboards(path, republish=False)

    def test_share_unowned_dash(self):
        dashboard = self.py_client.get_dashboard_by_id('5f7c79ae26e1201818bf479b', admin_access=True)
        user = self.py_client.get_users(first_name='nathan.giusti')
        assert len(dashboard.get_shares(admin_access=True)['sharesTo']) == 1
        assert len(dashboard.get_share_users_groups(admin_access=True)) == 1
        dashboard.add_share(user, 'view', False, admin_access=True)
        assert len(dashboard.get_shares(admin_access=True)['sharesTo']) == 2
        assert len(dashboard.get_share_users_groups(admin_access=True)) == 2
        dashboard.remove_shares(user, admin_access=True)
        assert len(dashboard.get_shares(admin_access=True)) == 1
        assert len(dashboard.get_share_users_groups(admin_access=True)) == 1


    @classmethod
    def tearDownClass(cls):
        cls.dashboard.remove_shares(cls.dashboard.get_share_users_groups())









