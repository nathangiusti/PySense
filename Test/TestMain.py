import unittest

from Test.PySenseDashboardTests import PySenseDashboardTests
from Test.PySenseElasticubeTests import PySenseElasticubeTests
from Test.PySenseGroupTests import PySenseGroupTests
from Test.PySenseTests import PySenseTests
from Test.PySenseWidgetTest import PySenseWidgetTest

scale_test_suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(PySenseWidgetTest),
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
