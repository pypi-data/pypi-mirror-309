# run_tests.py

import unittest

def run_all_tests():
    # Discover and run all tests in the 'tests' directory
    loader = unittest.TestLoader()
    tests = loader.discover(start_dir='tests')
    testRunner = unittest.runner.TextTestRunner()
    testRunner.run(tests)

if __name__ == '__main__':
    run_all_tests()
