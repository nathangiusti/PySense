import os
import unittest

from PySense import PySense


class PySenseWidgetTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('resources//TestConfig.yaml')
        cls.dashboard = cls.py_client.get_dashboards(name='PySense')[0]
        cls.widget = cls.dashboard.get_widgets()[0]
        cls.path = 'tmp//'

    def test_export_png(self):
        path = self.path + 'widget.png'
        self.widget.export_to_png(100, 100, path)
        os.remove(path)

    def test_getters(self):
        assert self.widget.get_oid() is not None
        assert self.widget.get_dashboard_id() is not None
        assert self.widget.get_json() is not None


if __name__ == '__main__':
    unittest.main()
