import json
import os
import unittest
import PySense

sample_dash_id = '5e0a36991f05044544883969'
sample_path = 'C:\\PySenseTests'
pivot_widget = '5e0a36991f05044544883969'


class PySenseTests(unittest.TestCase):
    def setUp(self):
        PySense.authenticate_by_file('C:\\PySenseConfig.yaml')

    def test_auth(self):
        assert PySense.check_authentication() is not None
        assert PySense.get_host() == 'http://localhost:8081'
        assert PySense.get_token() is not None


    def test_get_folders(self):
        temp = PySense.get_folders(name='PySense')
        assert len(temp) == 2
        assert temp[0]['name'] == 'PySense'


    def test_get_dashboards(self):
        ret = PySense.get_dashboards(parentFolder='PySense')
        assert ret[0]['title'] == 'PySense'
        assert len(ret) == 1
        f = open(sample_path + '\\' + sample_dash_id + '.dash', 'w')
        f.write(json.dumps(ret[0]))
        f.close()


    def test_get_folder_by_name(self):
        assert PySense.get_folder_by_name('PySense')['name'] == 'PySense'


    def test_get_dashboard_export_png(self):
        assert sample_path + '\\' + sample_dash_id + '.png' == \
               PySense.get_dashboard_export_png(sample_dash_id, sample_path + '\\' + sample_dash_id + '.png',
                                               includeTitle='true', includeFilters=True, includeDs=False, width=1000)
        os.remove(sample_path + '\\' + sample_dash_id + '.png')


    def test_get_dashboard_export_pdf(self):
        assert sample_path + '\\' + sample_dash_id + '.pdf' == \
               PySense.get_dashboard_export_pdf(sample_dash_id, sample_path + '\\' + sample_dash_id + '.pdf', 'A4',
                                               'portrait', 'asis', includeTitle='true', includeFilters=True,
                                               includeDs=False, widgetid=pivot_widget, preview=None, rowCount=None,
                                               showTitle=None, showFooter=None, title=None, titleSize=None,
                                               titlePosition=None)
        os.remove(sample_path + '\\' + sample_dash_id + '.pdf')


if __name__ == '__main__':
    unittest.main()
