<p align="center">
<a href="https://github.com/sashsinha/typed_input"><img alt="Typed Input Logo" src="https://raw.githubusercontent.com/sashsinha/typed_input/main/logo.png"></a>
</p>

<h1 align="center">Typed Input</h1>

<h3 align="center">Effortless type-safe user input for integers, floats, dates, and more...</h3>

<p align="center">
<a href="https://raw.githubusercontent.com/sashsinha/typed_input/main/LICENCE"><img alt="License: MIT" src="https://raw.githubusercontent.com/sashsinha/typed_input/main/license.svg"></a>
</p>


### Supported Functions:
- [`int_input`](#int_input---a)
- [`float_input`](#float_input)
- [`decimal_input`](#decimal_input)
- [`datetime_input`](#datetime_input)

Each function has this structure:

```python
<type>_input(
  prompt: str | None = None,
  min_value: <type> | None = None,
  max_value: <type> | None = None,
  default_value: <type> | None = None,
  type_error_message: str | None = None,
) -> <type>
```

#### Parameters:
- **`prompt`**: *(Optional)* Message displayed to the user when prompting for input.
- **`min_value` / `max_value`**: *(Optional)* Bounds for input validation.
- **`default_value`**: *(Optional)* Value returned if no input is provided. Must fall within bounds.
- **`type_error_message`**: *(Optional)* Error message shown when input cannot be converted to expected type. Defaults are provided for each function.

#### Default Type Error Messages:

| Function           | Default `type_error_message`                                                                                            |
|--------------------|--------------------------------------------------------------------------------------------------------------------------|
| `int_input`        | **Error**: You must enter a valid integer.                                                                              |
| `float_input`      | **Error**: You must enter a valid float.                                                                                |
| `decimal_input`    | **Error**: You must enter a valid Decimal.                                                                              |
| `datetime_input`   | **Error**: You must enter a valid datetime in valid ISO 8601 format e.g. YYYY-MM-DD.<br>See [documentation](https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat) for all allowed options.|

---

### Example Usage

#### `int_input` - Function for  Integer Input
```python
>>> int_input(prompt="Enter a number (1-10): ", min_value=1, max_value=10)
Enter a number (1-10): abc
Error: You must enter a valid integer.
Enter a number (1-10): 20
Error: Value must be between 1 and 10.
Enter a number (1-10): 5
5
```

#### Floating-Point Input
```python
>>> float_input(prompt="Enter a temperature (-50 to 50): ", min_value=-50.0, max_value=50.0)
Enter a temperature (-50 to 50): 
Error: You must enter a valid float.
Enter a temperature (-50 to 50): 100
Error: Value must be between -50.0 and 50.0.
Enter a temperature (-50 to 50): 22.5
22.5
```

#### Decimal Input
```python
>>> from decimal import Decimal
>>> decimal_input(prompt="Enter a price (min 0.01): ", min_value=Decimal("0.01"))
Enter a price (min 0.01): -10
Error: Value must be at least 0.01.
Enter a price (min 0.01): 19.99
Decimal('19.99')
```

#### Datetime Input
```python
>>> from datetime import datetime
>>> datetime_input(prompt="Enter a date (YYYY-MM-DD): ", min_value=datetime(2023, 1, 1))
Enter a date (YYYY-MM-DD): invalid
Error: You must enter a valid datetime in ISO 8601 format (e.g., YYYY-MM-DD).
Enter a date (YYYY-MM-DD): 2022-12-31
Error: Date must be on or after 2023-01-01.
Enter a date (YYYY-MM-DD): 2023-01-15
datetime.datetime(2023, 1, 15, 0, 0)
```
---

### ❌ Error Handling

All functions raise a `ValueError` for:
- **Invalid Range**: `min_value > max_value`.
- **Default Out of Bounds**: `default_value` outside `min_value`/`max_value`.

Example:
```python
>>> int_input(min_value=10, max_value=5)
Traceback (most recent call last):
  ...
ValueError: min_value (10) cannot be greater than max_value (5).
```

---

### 🛠️ Development

- Run formater: 
  - `uv run ruff check --select I --fix && uv run ruff format`
- Run type checking: 
  - `uv run mypy . `
- Run all unit tests:
  - `uv run typed_input_test.py`
- Run specific unit test:
  - `uv run python -m unittest int_input_test.py`

