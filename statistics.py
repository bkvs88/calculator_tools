"""statistics.py — Statistical helpers over collections of numbers.

Provides mean/average, median, and sum calculations with strict
validation of the input data.
"""

from .exceptions import (
    EmptyDataError,    # raised when no data is provided
    InvalidInputError, # raised when data contains non-numeric values
)


def _validate_data(data):
    """Validate and return ``data`` converted to a non-empty list of numbers.

    Raises:
        EmptyDataError: if ``data`` is None or empty.
        InvalidInputError: if ``data`` is a string or contains non-numbers.
    """
    if data is None:
        raise EmptyDataError("Data cannot be None")
    # Strings are iterable but are not a sensible collection of numbers.
    if isinstance(data, (str, bytes)):
        raise InvalidInputError("Data must be an iterable of numbers, got a string")
    try:
        values = list(data)
    except TypeError:
        raise InvalidInputError("Data must be an iterable of numbers")
    if not values:
        raise EmptyDataError("Data cannot be empty")
    for v in values:
        # bool is a subclass of int; reject it too.
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise InvalidInputError(f"Data contains non-numeric value: {v!r}")
    return values


def average(data):
    """Return the arithmetic mean of a collection of numbers."""
    values = _validate_data(data)
    return sum(values) / len(values)


def mean(data):
    """Alias for :func:`average` — returns the arithmetic mean."""
    return average(data)


def median(data):
    """Return the middle value of sorted ``data`` (average of the two middle values if even)."""
    values = sorted(_validate_data(data))
    n = len(values)
    mid = n // 2
    if n % 2 == 1:
        # Odd count: the single middle element.
        return values[mid]
    # Even count: average of the two middle elements.
    return (values[mid - 1] + values[mid]) / 2


def total(data):
    """Return the sum of all numbers in ``data``."""
    values = _validate_data(data)
    return sum(values)
