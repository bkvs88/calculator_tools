"""exceptions.py — Custom exception hierarchy for calculator_tools.

Defining our own exceptions lets callers catch package-specific errors
with a single base class ``CalculatorError`` while still being able to
distinguish the individual error types.
"""


class CalculatorError(Exception):
    """Base exception for the calculator_tools package.

    Every other exception in this package inherits from this class, so a
    caller can catch any package error with ``except CalculatorError``.
    """


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""


class InvalidInputError(CalculatorError):
    """Raised when input is not a valid number (e.g. a string or bool)."""


class UnsupportedOperationError(CalculatorError):
    """Raised when an operation, unit, or category is not supported."""


class EmptyDataError(CalculatorError):
    """Raised when an empty dataset is provided where data is required."""


class InvalidOperationError(CalculatorError):
    """Raised when an invalid operation is attempted on the calculator."""
