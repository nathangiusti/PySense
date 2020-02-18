import unittest
from Test.PySenseTests import PySenseTests
from Test.PySenseDashboardTests import PySenseDashboardTests

scale_test_suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(PySenseDashboardTests),
    unittest.TestLoader().loadTestsFromTestCase(PySenseTests)
])

def test_scale_suite():

    result = unittest.TestResult()
    runner = unittest.TextTestRunner()
    print(runner.run(scale_test_suite))


if __name__ == '__main__':
    test_scale_suite()
