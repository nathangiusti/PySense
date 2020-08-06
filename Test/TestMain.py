import unittest

from Test.PySenseConnectionTests import PySenseConnectionTests
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
    # unittest.TestLoader().loadTestsFromTestCase(PySenseConnectionTests),
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
    result = unittest.TestResult()
    runner = unittest.TextTestRunner()
    print(runner.run(scale_test_suite))


if __name__ == '__main__':
    test_scale_suite()
