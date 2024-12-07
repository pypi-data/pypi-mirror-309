import unittest

import datetime_input_test
import decimal_input_test
import float_input_test
import int_input_test


def main() -> None:
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  for module in [
    datetime_input_test,
    decimal_input_test,
    int_input_test,
    float_input_test,
  ]:
    suite.addTests(loader.loadTestsFromModule(module))
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)


if __name__ == '__main__':
  main()
