"""Effortless type-safe user input for integers, floats, dates, and more..."""

from __future__ import annotations

import decimal
import sys
from datetime import datetime
from decimal import Decimal
from typing import Any, Callable, TypeVar


def _get_python_version() -> str:
  """Returns the Python version in the format 'major.minor'."""
  return f'{sys.version_info.major}.{sys.version_info.minor}'


_FROMISOFORMAT_DOCS_URL = f'https://docs.python.org/{_get_python_version()}/library/datetime.html#datetime.datetime.fromisoformat'
_BASE_INVALID_TYPE_ERROR = 'Error: You must enter a valid'
_DEFAULT_INT_INPUT_TYPE_ERROR = f'{_BASE_INVALID_TYPE_ERROR} integer.'
_DEFAULT_FLOAT_INPUT_TYPE_ERROR = f'{_BASE_INVALID_TYPE_ERROR} float.'
_DEFAULT_DECIMAL_INPUT_TYPE_ERROR = f'{_BASE_INVALID_TYPE_ERROR} Decimal.'
_DEFAULT_DATETIME_INPUT_TYPE_ERROR = (
  f'{_BASE_INVALID_TYPE_ERROR} datetime in valid ISO 8601 format e.g. YYYY-MM-DD.\n'
  f'See {_FROMISOFORMAT_DOCS_URL} for all allowed options.'
)
_T = TypeVar('_T', int, float, Decimal, datetime)


def _generic_single_value_input(
  prompt: str | None,
  min_value: _T | None,
  max_value: _T | None,
  default_value: _T | None,
  type_error_message: str,
  conversion_function: Callable[[str], _T],
) -> _T:
  """Generic function that prompts for input until valid input of desired type.

  Args:
    prompt: A message displayed when prompting for input. If not provided, no
      prompt is shown.
    min_value: The minimum acceptable value for the input. If provided, the
      function will only accept values greater than or equal to this value.
    max_value: The maximum acceptable value for the input. If provided,
      function will only accept values less than or equal to this value.
    default_value: A value to be used when the user inputs an empty string. If
      not specified, empty input will not be allowed, and the user will be
      required to provide a valid input of the specified type.
    type_error_message: A custom error message displayed when the user enters a
      value not of the specified type.
    conversion_function: Function to try convert the user input string to the
      desired type.

  Returns:
    T: Validated input of the specified type, or the default value if it is set
      and the empty string is provided.

  Raises:
    ValueError: If both `min_value` and `max_value` are specified, and
      `min_value` is greater than `max_value`.
    ValueError: If `default_value` is specified but falls outside the range
      defined by `min_value` or `max_value`.
  """
  if min_value is not None and max_value is not None and min_value > max_value:
    raise ValueError(f'({min_value=}) is greater than ({max_value=}).')
  if default_value is not None:
    if min_value is not None and default_value < min_value:
      raise ValueError(f'({default_value=}) is less than ({min_value=}).')
    if max_value is not None and default_value > max_value:
      raise ValueError(f'({default_value=}) is greater than ({max_value=}).')
  while True:
    try:
      user_input = input(prompt) if prompt else input()
      if not user_input.strip() and default_value is not None:
        return default_value
      value = conversion_function(user_input)
      if min_value is not None and value < min_value:
        print(f'Error: Value must be at least {min_value}.')
        continue
      if max_value is not None and value > max_value:
        print(f'Error: Value must be at most {max_value}.')
        continue
      return value
    except (ValueError, decimal.DecimalException):
      print(type_error_message)


def int_input(
  prompt: str | None = None,
  min_value: int | None = None,
  max_value: int | None = None,
  default_value: int | None = None,
  type_error_message: str | None = None,
) -> int:
  """Prompts to enter an int, with optional default and range validation.

  Args:
    prompt: A message displayed when prompting for input. If not provided, no
      prompt is shown.
    min_value: The minimum acceptable value for the input. If provided, the
      function will only accept integers greater than or equal to this value.
    max_value: The maximum acceptable value for the input. If provided,
      function will only accept integers less than or equal to this value.
    default_value: A value to be used when the user inputs an empty string. If
      not specified, empty input will not be allowed, and the user will be
      required to provide a valid integer.
    type_error_message: A custom error message displayed when the user enters a
      non-integer value. The default message if not provided is:
      'Error: You must enter a valid integer.'

  Returns:
    int: The validated integer input entered, or the default value
      if it is set and the empty string is provided.

  Raises:
    ValueError: If both `min_value` and `max_value` are specified, and
      `min_value` is greater than `max_value`.
    ValueError: If `default_value` is specified but falls outside the range
      defined by `min_value` or `max_value`.
  """
  if not type_error_message:
    type_error_message = _DEFAULT_INT_INPUT_TYPE_ERROR
  return _generic_single_value_input(
    prompt=prompt,
    min_value=min_value,
    max_value=max_value,
    default_value=default_value,
    type_error_message=type_error_message,
    conversion_function=int,
  )


def float_input(
  prompt: str | None = None,
  min_value: float | None = None,
  max_value: float | None = None,
  default_value: float | None = None,
  type_error_message: str | None = None,
) -> float:
  """Prompts to enter a float, with optional default and range validation.

  Args:
    prompt: A message displayed when prompting for input. If not provided, no
      prompt is shown.
    min_value: The minimum acceptable value for the input. If provided, the
      function will only accept floats greater than or equal to this value.
    max_value: The maximum acceptable value for the input. If provided,
      function will only accept floats less than or equal to this value.
    default_value: A value to be used when the user inputs an empty string. If
      not specified, empty input will not be allowed, and the user will be
      required to provide a valid float.
    type_error_message: A custom error message displayed when the user enters a
      non-float value. The default message if not provided is:
      'Error: You must enter a valid float.'

  Returns:
    float: The validated float input entered, or the default value
      if it is set and the empty string is provided.

  Raises:
    ValueError: If both `min_value` and `max_value` are specified, and
      `min_value` is greater than `max_value`.
    ValueError: If `default_value` is specified but falls outside the range
      defined by `min_value` or `max_value`.
  """
  if not type_error_message:
    type_error_message = _DEFAULT_FLOAT_INPUT_TYPE_ERROR
  return _generic_single_value_input(
    prompt=prompt,
    min_value=min_value,
    max_value=max_value,
    default_value=default_value,
    type_error_message=type_error_message,
    conversion_function=float,
  )


def decimal_input(
  prompt: str | None = None,
  min_value: Decimal | None = None,
  max_value: Decimal | None = None,
  default_value: Decimal | None = None,
  type_error_message: str | None = None,
) -> Decimal:
  """Prompts to enter a Decimal, with optional default and range validation.

  Args:
    prompt: A message displayed when prompting for input. If not provided, no
      prompt is shown.
    min_value: The minimum acceptable value for the input. If provided, the
      function will only accept Decimals greater than or equal to this value.
    max_value: The maximum acceptable value for the input. If provided,
      function will only accept Decimals less than or equal to this value.
    default_value: A value to be used when the user inputs an empty string. If
      not specified, empty input will not be allowed, and the user will be
      required to provide a valid Decimal.
    type_error_message: A custom error message displayed when the user enters a
      non-Decimal value. The default message if not provided is:
      'Error: You must enter a valid Decimal.'

  Returns:
    Decimal: The validated Decimal input entered, or the default value
      if it is set and the empty string is provided.

  Raises:
    ValueError: If both `min_value` and `max_value` are specified, and
      `min_value` is greater than `max_value`.
    ValueError: If `default_value` is specified but falls outside the range
      defined by `min_value` or `max_value`.
  """
  if not type_error_message:
    type_error_message = _DEFAULT_DECIMAL_INPUT_TYPE_ERROR
  return _generic_single_value_input(
    prompt=prompt,
    min_value=min_value,
    max_value=max_value,
    default_value=default_value,
    type_error_message=type_error_message,
    conversion_function=Decimal,
  )


def datetime_input(
  prompt: str | None = None,
  min_value: datetime | None = None,
  max_value: datetime | None = None,
  default_value: datetime | None = None,
  type_error_message: str | None = None,
) -> datetime:
  """Prompts to enter a datetime, with optional default and range validation.

  Args:
    prompt: A message displayed when prompting for input. If not provided, no
      prompt is shown.
    min_value: The minimum acceptable value for the input. If provided, the
      function will only accept datetimes greater than or equal to this value.
    max_value: The maximum acceptable value for the input. If provided,
      function will only accept datetimes less than or equal to this value.
    default_value: A value to be used when the user inputs an empty string. If
      not specified, empty input will not be allowed, and the user will be
      required to provide a valid datetime.
    type_error_message: A custom error message displayed when the user enters a
      invalid datetime value. The default message if not provided is:
      'Error: You must enter a valid datetime in valid ISO 8601 format e.g. YYYY-MM-DD.'
      Along with a link to the the other allowed format options for the python
      version being used (Python 3.11 introduced more allowed formats).

  Returns:
    Decimal: The validated Decimal input entered, or the default value
      if it is set and the empty string is provided.

  Raises:
    ValueError: If both `min_value` and `max_value` are specified, and
      `min_value` is greater than `max_value`.
    ValueError: If `default_value` is specified but falls outside the range
      defined by `min_value` or `max_value`.
  """
  if not type_error_message:
    type_error_message = _DEFAULT_DATETIME_INPUT_TYPE_ERROR
  return _generic_single_value_input(
    prompt=prompt,
    min_value=min_value,
    max_value=max_value,
    default_value=default_value,
    type_error_message=type_error_message,
    conversion_function=datetime.fromisoformat,
  )
