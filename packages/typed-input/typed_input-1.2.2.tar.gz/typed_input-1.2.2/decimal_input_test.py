import io
import unittest
from decimal import Decimal
from unittest import mock

from typed_input import decimal_input


class DecimalInputTest(unittest.TestCase):
  @mock.patch('builtins.input', return_value='42.5')
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_valid_input_no_constraints(self, mock_stdout, mock_input):
    self.assertEqual(decimal_input(), Decimal('42.5'))
    mock_input.assert_called_once_with()
    self.assertEqual(mock_stdout.getvalue().strip(), '')

  @mock.patch('builtins.input', return_value='42.5')
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_valid_input_with_prompt(self, mock_stdout, mock_input):
    self.assertEqual(decimal_input(prompt='Enter a Decimal: '), Decimal('42.5'))
    mock_input.assert_called_once_with('Enter a Decimal: ')
    self.assertEqual(mock_stdout.getvalue().strip(), '')

  @mock.patch('builtins.input', side_effect=['abc', '42.5'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_invalid_input_retry(self, mock_stdout, mock_input):
    self.assertEqual(decimal_input(), Decimal('42.5'))
    self.assertEqual(mock_input.call_count, 2)
    self.assertIn(
      'Error: You must enter a valid Decimal.', mock_stdout.getvalue()
    )

  @mock.patch('builtins.input', side_effect=['3.0', '5.0'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_min_value_violation(self, mock_stdout, mock_input):
    self.assertEqual(decimal_input(min_value=Decimal('5.0')), Decimal('5.0'))
    self.assertEqual(mock_input.call_count, 2)
    self.assertIn('Error: Value must be at least 5.0.', mock_stdout.getvalue())

  @mock.patch('builtins.input', side_effect=['10.0', '8.0'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_max_value_violation(self, mock_stdout, mock_input):
    self.assertEqual(decimal_input(max_value=Decimal('8.0')), Decimal('8.0'))
    self.assertEqual(mock_input.call_count, 2)
    self.assertIn('Error: Value must be at most 8.0.', mock_stdout.getvalue())

  @mock.patch('builtins.input', side_effect=['2.0', '12.0', '8.0'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_min_and_max_value_violation(self, mock_stdout, mock_input):
    self.assertEqual(
      decimal_input(min_value=Decimal('5.0'), max_value=Decimal('10.0')),
      Decimal('8.0'),
    )
    self.assertEqual(mock_input.call_count, 3)
    self.assertIn('Error: Value must be at least 5.0.', mock_stdout.getvalue())
    self.assertIn('Error: Value must be at most 10.0.', mock_stdout.getvalue())

  @mock.patch('builtins.input', side_effect=['abc', '3.0', '5.0'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_invalid_input_then_out_of_range(self, mock_stdout, mock_input):
    self.assertEqual(decimal_input(min_value=Decimal('5.0')), Decimal('5.0'))
    self.assertEqual(mock_input.call_count, 3)
    self.assertIn(
      'Error: You must enter a valid Decimal.', mock_stdout.getvalue()
    )
    self.assertIn('Error: Value must be at least 5.0.', mock_stdout.getvalue())

  @mock.patch('builtins.input', side_effect=[''])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_default_value_used_when_input_empty(
    self, usued_mock_stdout, mock_input
  ):
    self.assertEqual(
      decimal_input(default_value=Decimal('10.5')), Decimal('10.5')
    )
    mock_input.assert_called_once_with()

  @mock.patch('builtins.input', side_effect=['abc', '42.5'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_custom_type_error_message(self, mock_stdout, unused_mock_input):
    self.assertEqual(
      decimal_input(type_error_message='Must provide a valid height.'),
      Decimal('42.5'),
    )
    self.assertIn('Must provide a valid height.', mock_stdout.getvalue())

  def test_error_raised_when_min_value_greater_than_max_value(self):
    with self.assertRaises(ValueError) as context:
      decimal_input(min_value=Decimal('2.0'), max_value=Decimal('1.0'))
    self.assertEqual(
      str(context.exception),
      "(min_value=Decimal('2.0')) is greater than (max_value=Decimal('1.0')).",
    )

  def test_error_raised_when_default_value_less_than_min_value(self):
    with self.assertRaises(ValueError) as context:
      decimal_input(min_value=Decimal('2.0'), default_value=Decimal('1.0'))
    self.assertEqual(
      str(context.exception),
      "(default_value=Decimal('1.0')) is less than (min_value=Decimal('2.0')).",
    )

  def test_error_raised_when_default_value_greater_than_max_value(self):
    with self.assertRaises(ValueError) as context:
      decimal_input(max_value=Decimal('1.0'), default_value=Decimal('2.0'))
    self.assertEqual(
      str(context.exception),
      "(default_value=Decimal('2.0')) is greater than (max_value=Decimal('1.0')).",
    )


if __name__ == '__main__':
  unittest.main()
