import unittest

import PySense.PySense as PySense


class PySenseWidgetTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('//Users//nathan.giusti//Documents//PySense//VmConfig.yaml')
        cls.dashboard = cls.py_client.get_dashboards(name='PySense')[0]
        cls.widget = cls.dashboard.get_widgets()[0]

    def test_export_png(self):
        self.widget.export_to_png(100, 100)

    def test_getters(self):
        assert self.widget.get_id() is not None
        assert self.widget.get_dashboard_id() is not None
        assert self.widget.get_json() is not None


if __name__ == '__main__':
    unittest.main()
