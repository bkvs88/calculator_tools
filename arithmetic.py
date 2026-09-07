"""arithmetic.py — Basic arithmetic and percentage operations.

This module provides simple, validated math functions used as the
foundation for the calculator_tools package.
"""

from .exceptions import (
    DivisionByZeroError,       # raised when dividing by zero
    InvalidInputError,         # raised when inputs are not numbers
    UnsupportedOperationError, # raised for unknown operations
)


def _validate_number(value, name="value"):
    """Ensure ``value`` is a real number (int/float), not a bool or string.

    Raises:
        InvalidInputError: if ``value`` is not a valid number.
    """
    # bool is a subclass of int in Python, so reject it explicitly.
    if isinstance(value, bool):
        raise InvalidInputError(f"{name} must be a number, got bool")
    if not isinstance(value, (int, float)):
        raise InvalidInputError(f"{name} must be a number, got {type(value).__name__}")


def add(a, b):
    """Return the sum of two numbers ``a`` and ``b``."""
    _validate_number(a, "a")
    _validate_number(b, "b")
    return a + b


def subtract(a, b):
    """Return the difference of ``a`` minus ``b``."""
    _validate_number(a, "a")
    _validate_number(b, "b")
    return a - b


def multiply(a, b):
    """Return the product of two numbers ``a`` and ``b``."""
    _validate_number(a, "a")
    _validate_number(b, "b")
    return a * b


def divide(a, b):
    """Return ``a`` divided by ``b``.

    Raises:
        DivisionByZeroError: if ``b`` is zero.
    """
    _validate_number(a, "a")
    _validate_number(b, "b")
    if b == 0:
        raise DivisionByZeroError("Cannot divide by zero")
    return a / b


def percentage(part, whole):
    """Return ``part`` as a percentage of ``whole``.

    Example: percentage(10, 50) -> 20.0

    Raises:
        DivisionByZeroError: if ``whole`` is zero.
    """
    _validate_number(part, "part")
    _validate_number(whole, "whole")
    if whole == 0:
        raise DivisionByZeroError("Whole cannot be zero when calculating percentage")
    return (part / whole) * 100


def power(base, exponent):
    """Return ``base`` raised to the power of ``exponent``."""
    _validate_number(base, "base")
    _validate_number(exponent, "exponent")
    return base ** exponent


def modulo(a, b):
    """Return the remainder of dividing ``a`` by ``b``.

    Raises:
        DivisionByZeroError: if ``b`` is zero.
    """
    _validate_number(a, "a")
    _validate_number(b, "b")
    if b == 0:
        raise DivisionByZeroError("Cannot take modulo by zero")
    return a % b


def calculate(operator, a, b=None):
    """Dispatch to the right arithmetic function using a string operator.

    Supported operators: add/+, subtract/-, multiply/*, divide//,
    power/**, modulo/%.
    """
    op = str(operator).lower()
    # Map human-readable names and symbols to the functions above.
    operations = {
        "add": add,
        "+": add,
        "subtract": subtract,
        "-": subtract,
        "multiply": multiply,
        "*": multiply,
        "divide": divide,
        "/": divide,
        "power": power,
        "**": power,
        "modulo": modulo,
        "%": modulo,
    }
    if op not in operations:
        raise UnsupportedOperationError(f"Unsupported operation: {operator}")
    return operations[op](a, b)
