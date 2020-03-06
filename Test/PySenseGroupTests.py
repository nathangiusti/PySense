import unittest
from PySense import PySense


class PySenseGroupTests(unittest.TestCase):
    def setUp(self):
        self.pyClient = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        self.sample_path = 'C:\\PySense\\'
        self.group = self.pyClient.get_dashboards(parent_folder_name='PySense')[0]


if __name__ == '__main__':
    unittest.main()

