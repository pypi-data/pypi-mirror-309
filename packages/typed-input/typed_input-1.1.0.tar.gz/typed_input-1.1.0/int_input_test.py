import io
import unittest
from unittest import mock

from typed_input import int_input


class IntInputTest(unittest.TestCase):
  @mock.patch('builtins.input', return_value='42')
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_valid_input_no_constraints(self, mock_stdout, mock_input):
    self.assertEqual(int_input(), 42)
    mock_input.assert_called_once_with()
    self.assertEqual(mock_stdout.getvalue().strip(), '')

  @mock.patch('builtins.input', return_value='42')
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_valid_input_with_prompt(self, mock_stdout, mock_input):
    self.assertEqual(int_input(prompt='Enter an integer: '), 42)
    mock_input.assert_called_once_with('Enter an integer: ')
    self.assertEqual(mock_stdout.getvalue().strip(), '')

  @mock.patch('builtins.input', side_effect=['abc', '42'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_invalid_input_retry(self, mock_stdout, mock_input):
    self.assertEqual(int_input(), 42)
    self.assertEqual(mock_input.call_count, 2)
    self.assertIn(
      'Error: You must enter a valid integer.', mock_stdout.getvalue()
    )

  @mock.patch('builtins.input', side_effect=['3', '5'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_min_value_violation(self, mock_stdout, mock_input):
    self.assertEqual(int_input(min_value=5), 5)
    self.assertEqual(mock_input.call_count, 2)
    self.assertIn('Error: Value must be at least 5.', mock_stdout.getvalue())

  @mock.patch('builtins.input', side_effect=['10', '8'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_max_value_violation(self, mock_stdout, mock_input):
    self.assertEqual(int_input(max_value=8), 8)
    self.assertEqual(mock_input.call_count, 2)
    self.assertIn('Error: Value must be at most 8.', mock_stdout.getvalue())

  @mock.patch('builtins.input', side_effect=['2', '12', '8'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_min_and_max_value_violation(self, mock_stdout, mock_input):
    self.assertEqual(int_input(min_value=5, max_value=10), 8)
    self.assertEqual(mock_input.call_count, 3)
    self.assertIn('Error: Value must be at least 5.', mock_stdout.getvalue())
    self.assertIn('Error: Value must be at most 10.', mock_stdout.getvalue())

  @mock.patch('builtins.input', side_effect=['abc', '3', '5'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_invalid_input_then_out_of_range(self, mock_stdout, mock_input):
    self.assertEqual(int_input(min_value=5), 5)
    self.assertEqual(mock_input.call_count, 3)
    self.assertIn(
      'Error: You must enter a valid integer.', mock_stdout.getvalue()
    )
    self.assertIn('Error: Value must be at least 5.', mock_stdout.getvalue())

  @mock.patch('builtins.input', side_effect=[''])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_default_value_used_when_input_empty(
    self, unused_mock_stdout, mock_input
  ):
    self.assertEqual(int_input(default_value=10), 10)
    mock_input.assert_called_once_with()

  @mock.patch('builtins.input', side_effect=['abc', '42'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_custom_type_error_message(self, mock_stdout, unused_mock_input):
    self.assertEqual(
      int_input(type_error_message='Must provide a valid age.'), 42
    )
    self.assertIn('Must provide a valid age.', mock_stdout.getvalue())

  @mock.patch('builtins.input', side_effect=['3.1', '3.0', '3.', '5'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_float_input_not_allowed(self, mock_stdout, mock_input):
    self.assertEqual(int_input(), 5)
    self.assertEqual(mock_input.call_count, 4)
    self.assertIn(
      '\n'.join(['Error: You must enter a valid integer.'] * 3),
      mock_stdout.getvalue(),
    )

  def test_error_raised_when_min_value_greater_than_max_value(self):
    with self.assertRaises(ValueError) as context:
      int_input(min_value=2, max_value=1)
    self.assertEqual(
      str(context.exception), '(min_value=2) is greater than (max_value=1).'
    )

  def test_error_raised_when_default_value_less_than_min_value(self):
    with self.assertRaises(ValueError) as context:
      int_input(min_value=2, default_value=1)
    self.assertEqual(
      str(context.exception), '(default_value=1) is less than (min_value=2).'
    )

  def test_error_raised_when_default_value_greater_than_max_value(self):
    with self.assertRaises(ValueError) as context:
      int_input(max_value=1, default_value=2)
    self.assertEqual(
      str(context.exception), '(default_value=2) is greater than (max_value=1).'
    )


if __name__ == '__main__':
  unittest.main()
