import os
import unittest
import urllib3

from PySense import PySense, PySenseException, SisenseRole
from Test.PySenseDashboardTests import PySenseDashboardTests
from Test.PySenseDataModelTests import PySenseDataModelTests
from Test.PySenseDataSetTests import PySenseDataSetTests
from Test.PySenseElasticubeTests import PySenseElasticubeTests
from Test.PySenseFolderTests import PySenseFolderTests
from Test.PySenseGroupTests import PySenseGroupTests
from Test.PySenseLinuxTests import PySenseLinuxTests
from Test.PySensePluginTests import PySensePluginTests
from Test.PySenseRuleTests import PySenseRuleTests
from Test.PySenseTableTests import PySenseTableTests
from Test.PySenseTests import PySenseTests
from Test.PySenseUserTests import PySenseUserTests
from Test.PySenseWidgetTests import PySenseWidgetTests
from Test.PySenseWindowsTest import PySenseWindowsTests


def prepare_test_suite():
    scale_test_suite = [

        unittest.TestLoader().loadTestsFromTestCase(PySenseUserTests),
        unittest.TestLoader().loadTestsFromTestCase(PySenseRuleTests),
        unittest.TestLoader().loadTestsFromTestCase(PySenseFolderTests),
        unittest.TestLoader().loadTestsFromTestCase(PySensePluginTests),
        unittest.TestLoader().loadTestsFromTestCase(PySenseWidgetTests),
        unittest.TestLoader().loadTestsFromTestCase(PySenseGroupTests),
        unittest.TestLoader().loadTestsFromTestCase(PySenseElasticubeTests),
        unittest.TestLoader().loadTestsFromTestCase(PySenseDashboardTests),
        unittest.TestLoader().loadTestsFromTestCase(PySenseTests)
    ]
    linux_tests = [
        unittest.TestLoader().loadTestsFromTestCase(PySenseDataSetTests),
        unittest.TestLoader().loadTestsFromTestCase(PySenseTableTests),
        unittest.TestLoader().loadTestsFromTestCase(PySenseDataModelTests),
        unittest.TestLoader().loadTestsFromTestCase(PySenseLinuxTests)
    ]
    windows_tests = [
        unittest.TestLoader().loadTestsFromTestCase(PySenseWindowsTests)
    ]
    if os.path.exists('resources//LinuxConfig.yaml'):
        does_cube_exist(PySense.authenticate_by_file('resources//LinuxConfig.yaml'), 'PySense', 'LinuxConfig')
        scale_test_suite = scale_test_suite + linux_tests
    if os.path.exists('resources//WindowsConfig.yaml'):
        does_cube_exist(PySense.authenticate_by_file('resources//WindowsConfig.yaml'), 'PySense', 'WindowsConfig')
        scale_test_suite = scale_test_suite + windows_tests

    return unittest.TestSuite(scale_test_suite)


def does_cube_exist(py_client, cube_name, server_name):
    if py_client.get_elasticube_by_name(cube_name) is None:
        raise PySenseException.PySenseException(
            'No PySense Elasticube found on {} server.'.format(server_name)
        )


def test_scale_suite():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    result = unittest.TestResult()
    runner = unittest.TextTestRunner()
    # Set up linux instance for testing
    py_client = PySense.authenticate_by_file('resources//TestConfig.yaml')

    does_cube_exist(py_client, 'PySense', 'TestConfig')

    dash = py_client.import_dashboards('resources//PySense.dash')

    user = py_client.get_users(user_name='pysensetest@sisense.com')
    if len(user) == 0:
        user = py_client.add_user('pysensetest@sisense.com', SisenseRole.Role.DESIGNER)
    else:
        user = user[0]

    user2 = py_client.get_users(user_name='pysensetest2@sisense.com')
    if len(user2) == 0:
        user2 = py_client.add_user('pysensetest2@sisense.com', SisenseRole.Role.DESIGNER)
    else:
        user2 = user2[0]

    group = py_client.get_groups(name='PySense')
    if len(group) == 0:
        group = py_client.add_groups('PySense')
    else:
        group = group[0]

    folder = py_client.get_folders(name='PySense')
    if len(folder) == 0:
        folder = py_client.add_folder('PySense')
    else:
        folder = folder[0]

    scale_test_suite = prepare_test_suite()

    print(runner.run(scale_test_suite))

    # Remove test assets
    py_client.delete_dashboards(dash)
    py_client.delete_users([user, user2])
    py_client.delete_groups(group)
    py_client.delete_folders(folder)


if __name__ == '__main__':
    test_scale_suite()
