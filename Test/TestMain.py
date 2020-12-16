import unittest
import urllib3

from PySense import PySense, SisenseRole
from Test.PySenseDashboardTests import PySenseDashboardTests
from Test.PySenseDataModelTests import PySenseDataModelTests
from Test.PySenseDataSetTests import PySenseDataSetTests
from Test.PySenseElasticubeTests import PySenseElasticubeTests
from Test.PySenseFolderTests import PySenseFolderTests
from Test.PySenseGroupTests import PySenseGroupTests
from Test.PySensePluginTests import PySensePluginTests
from Test.PySenseRuleTests import PySenseRuleTests
from Test.PySenseTableTests import PySenseTableTests
from Test.PySenseTests import PySenseTests
from Test.PySenseUserTests import PySenseUserTests
from Test.PySenseWidgetTests import PySenseWidgetTests

scale_test_suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(PySenseDataSetTests),
    unittest.TestLoader().loadTestsFromTestCase(PySenseTableTests),
    unittest.TestLoader().loadTestsFromTestCase(PySenseDataModelTests),
    unittest.TestLoader().loadTestsFromTestCase(PySenseUserTests),
    unittest.TestLoader().loadTestsFromTestCase(PySenseRuleTests),
    unittest.TestLoader().loadTestsFromTestCase(PySenseFolderTests),
    unittest.TestLoader().loadTestsFromTestCase(PySensePluginTests),
    unittest.TestLoader().loadTestsFromTestCase(PySenseWidgetTests),
    unittest.TestLoader().loadTestsFromTestCase(PySenseGroupTests),
    unittest.TestLoader().loadTestsFromTestCase(PySenseElasticubeTests),
    unittest.TestLoader().loadTestsFromTestCase(PySenseDashboardTests),
    unittest.TestLoader().loadTestsFromTestCase(PySenseTests)
])


def test_scale_suite():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    result = unittest.TestResult()
    runner = unittest.TextTestRunner()
    # Set up linux instance for testing
    py_client = PySense.authenticate_by_file('resources//LinuxConfig.yaml')

    model = py_client.get_data_models(title='PySense')
    if model is None:
        model = py_client.import_schema('resources//PySense.smodel', title='PySense')
    dash = py_client.import_dashboards('resources//PySense.dash')

    # Set up windows instance for testing
    py_client_win = PySense.authenticate_by_file('resources//WindowsConfig.yaml')
    dash_win = py_client_win.import_dashboards('resources//PySense.dash')

    user_win = py_client_win.get_users(user_name='pysensetest@sisense.com')
    if len(user_win) == 0:
        user_win = py_client_win.add_user('pysensetest@sisense.com', SisenseRole.Role.DESIGNER)
    else:
        user_win = user_win[0]

    user_win2 = py_client_win.get_users(user_name='pysensetest2@sisense.com')
    if len(user_win2) == 0:
        user_win2 = py_client_win.add_user('pysensetest2@sisense.com', SisenseRole.Role.DESIGNER)
    else:
        user_win2 = user_win2[0]

    group_win = py_client_win.get_groups(name='PySense')
    if len(group_win) == 0:
        group_win = py_client_win.add_groups('PySense')
    else:
        group_win = group_win[0]

    folder_win = py_client_win.get_folders(name='PySense')
    if len(folder_win) == 0:
        folder_win = py_client_win.add_folder('PySense')
    else:
        folder_win = folder_win[0]

    print(runner.run(scale_test_suite))

    # Remove test assets
    py_client.delete_dashboards(dash)
    py_client.delete_data_model(model)
    py_client_win.delete_dashboards(dash_win)
    py_client_win.delete_users([user_win, user_win2])
    py_client_win.delete_groups(group_win)
    py_client_win.delete_folders(folder_win)


if __name__ == '__main__':
    test_scale_suite()
