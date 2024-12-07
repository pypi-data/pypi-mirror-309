import io
import sys
import unittest
from datetime import datetime
from unittest import mock

from parameterized import parameterized

from typed_input import datetime_input


def _get_python_version() -> str:
  """Returns the Python version in the format 'major.minor'."""
  return f'{sys.version_info.major}.{sys.version_info.minor}'


class DateTimeInputTest(unittest.TestCase):
  @mock.patch('builtins.input', return_value='2023-11-15')
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_valid_input_no_constraints(self, mock_stdout, mock_input):
    self.assertEqual(datetime_input(), datetime.fromisoformat('2023-11-15'))
    mock_input.assert_called_once_with()
    self.assertEqual(mock_stdout.getvalue().strip(), '')

  @mock.patch('builtins.input', return_value='2023-11-15')
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_valid_input_with_prompt(self, mock_stdout, mock_input):
    self.assertEqual(
      datetime_input(prompt='Enter a ISO 8601 datetime: '),
      datetime.fromisoformat('2023-11-15'),
    )
    mock_input.assert_called_once_with('Enter a ISO 8601 datetime: ')
    self.assertEqual(mock_stdout.getvalue().strip(), '')

  @mock.patch('builtins.input', side_effect=['invalid', '2023-11-15'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_invalid_input_retry(self, mock_stdout, mock_input):
    self.assertEqual(datetime_input(), datetime.fromisoformat('2023-11-15'))
    self.assertEqual(mock_input.call_count, 2)
    fromisoformat_docs_url = f'https://docs.python.org/{_get_python_version()}/library/datetime.html#datetime.datetime.fromisoformat'
    datetime_error = (
      f'Error: You must enter a valid datetime in valid ISO 8601 format e.g. YYYY-MM-DD.\n'
      f'See {fromisoformat_docs_url} for all allowed options.'
    )
    self.assertIn(datetime_error, mock_stdout.getvalue())

  @mock.patch('builtins.input', side_effect=['2023-11-01', '2023-11-20'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_min_value_violation(self, mock_stdout, mock_input):
    self.assertEqual(
      datetime_input(min_value=datetime.fromisoformat('2023-11-15')),
      datetime.fromisoformat('2023-11-20'),
    )
    self.assertEqual(mock_input.call_count, 2)
    self.assertIn(
      'Error: Value must be at least 2023-11-15 00:00:00.',
      mock_stdout.getvalue(),
    )

  @mock.patch('builtins.input', side_effect=['2023-11-30', '2023-11-25'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_max_value_violation(self, mock_stdout, mock_input):
    self.assertEqual(
      datetime_input(max_value=datetime.fromisoformat('2023-11-25')),
      datetime.fromisoformat('2023-11-25'),
    )
    self.assertEqual(mock_input.call_count, 2)
    self.assertIn(
      'Error: Value must be at most 2023-11-25 00:00:00.',
      mock_stdout.getvalue(),
    )

  @mock.patch('builtins.input', return_value='')
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_default_value_used_when_input_empty(
    self, usued_mock_stdout, mock_input
  ):
    self.assertEqual(
      datetime_input(default_value=datetime.fromisoformat('2023-11-15')),
      datetime.fromisoformat('2023-11-15'),
    )
    mock_input.assert_called_once_with()

  @mock.patch('builtins.input', side_effect=['invalid', '2023-11-15'])
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_custom_type_error_message(self, mock_stdout, unused_mock_input):
    self.assertEqual(
      datetime_input(type_error_message='Must provide a valid datetime.'),
      datetime.fromisoformat('2023-11-15'),
    )
    self.assertIn('Must provide a valid datetime.', mock_stdout.getvalue())

  def test_error_raised_when_min_value_greater_than_max_value(self):
    with self.assertRaises(ValueError) as context:
      datetime_input(
        min_value=datetime.fromisoformat('2023-11-15'),
        max_value=datetime.fromisoformat('2023-11-01'),
      )
    self.assertEqual(
      str(context.exception),
      '(min_value=datetime.datetime(2023, 11, 15, 0, 0)) is greater than '
      '(max_value=datetime.datetime(2023, 11, 1, 0, 0)).',
    )

  def test_error_raised_when_default_value_less_than_min_value(self):
    with self.assertRaises(ValueError) as context:
      datetime_input(
        min_value=datetime.fromisoformat('2023-11-15'),
        default_value=datetime.fromisoformat('2023-11-01'),
      )
    self.assertEqual(
      str(context.exception),
      '(default_value=datetime.datetime(2023, 11, 1, 0, 0)) is less than '
      '(min_value=datetime.datetime(2023, 11, 15, 0, 0)).',
    )

  def test_error_raised_when_default_value_greater_than_max_value(self):
    with self.assertRaises(ValueError) as context:
      datetime_input(
        max_value=datetime.fromisoformat('2023-11-01'),
        default_value=datetime.fromisoformat('2023-11-15'),
      )
    self.assertEqual(
      str(context.exception),
      '(default_value=datetime.datetime(2023, 11, 15, 0, 0)) is greater than '
      '(max_value=datetime.datetime(2023, 11, 1, 0, 0)).',
    )

  # See https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat
  # for all supported formats. Note Python 3.11 added new supported formats.
  @parameterized.expand(
    [
      ('%Y-%m-%d %H:%M:%S', '2023-11-15 15:30:00'),
      ('%Y-%m-%dT%H:%M', '2023-11-15T15:30'),
      ('%Y-%m-%dT%H:%M:%S', '2023-11-15T15:30:00'),
      ('%Y-%m-%dT%H:%M:%S.%f', '2023-11-15T15:30:00.123456'),
      ('%Y-%m-%dT%H:%M:%S%z', '2023-11-15T15:30:00-05:00'),
    ]
  )
  @mock.patch('sys.stdout', new_callable=io.StringIO)
  def test_iso_8601_formats(self, unused_name, iso_format, mock_stdout):
    with mock.patch('builtins.input', return_value=iso_format):
      self.assertEqual(datetime_input(), datetime.fromisoformat(iso_format))
      self.assertIn('', mock_stdout.getvalue())


if __name__ == '__main__':
  unittest.main(buffer=False)
