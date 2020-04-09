import unittest

import PySense.PySense as PySense


class PySenseWidgetTest(unittest.TestCase):
    def setUp(self):
        self.py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        self.dashboard = self.py_client.get_dashboards(parent_folder_name='PySense')[0]
        self.widget = self.dashboard.get_widgets()[0]

    def test_export_png(self):
        self.widget.export_to_png(100, 100)
    
    
if __name__ == '__main__':
    unittest.main()