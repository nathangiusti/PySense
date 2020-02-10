import unittest
import PySense


class PySenseTests(unittest.TestCase):

    def test_auth(self):
        assert PySense.authenticate_by_file('C:\\PySenseConfig.yaml')
        ret = PySense.check_authentication()
        assert ret['host'] == 'http://localhost:8081'
        assert ret['token'] is not None

    def test_get_folders(self):
        temp = PySense.get_folders(name='PySense')
        assert len(temp) == 2
        assert temp[0]['name'] == 'PySense'

    def test_get_dashboards(self):
        ret = PySense.get_folders(name='PySense')
        assert ret[0]['name'] == 'PySense'
        folder_id = ret[0]['oid']
        ret = PySense.get_dashboards(parentFolder=folder_id)
        assert ret[0]['title'] == 'PySense'
        assert len(ret) == 1

    def test_get_folder_by_name(self):
        assert PySense.get_folder_by_name('PySense')['name'] == 'PySense'


if __name__ == '__main__':
    unittest.main()
