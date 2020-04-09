import unittest

import PySense.PySense as PySense


class PySenseGroupTests(unittest.TestCase):
    def setUp(self):
        self.py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        self.sample_path = 'C:\\PySense\\'
        self.group = self.py_client.get_dashboards(parent_folder_name='PySense')[0]


if __name__ == '__main__':
    unittest.main()

