"""calculator_tools — A reusable arithmetic, statistics, and conversion package.

This module is the package entry point. It re-exports the public API from
each submodule so users can write ``from calculator_tools import add``
instead of reaching into individual modules.
"""

from .arithmetic import (
    add,                 # sum of two numbers
    subtract,            # difference of two numbers
    multiply,            # product of two numbers
    divide,              # quotient, guarding against division by zero
    percentage,          # part as a percentage of whole
    power,               # base raised to an exponent
    modulo,              # remainder of a division
    calculate,           # dispatch on a string operator
)
from .statistics import (
    average,             # arithmetic mean
    mean,                # alias for average
    median,              # middle value of sorted data
    total,               # sum of all values
)
from .converter import (
    celsius_to_fahrenheit,   # C -> F
    celsius_to_kelvin,       # C -> K
    fahrenheit_to_celsius,   # F -> C
    fahrenheit_to_kelvin,    # F -> K
    kelvin_to_celsius,       # K -> C
    kelvin_to_fahrenheit,    # K -> F
    convert_temperature,     # generic temperature conversion
    convert_unit,            # generic length/mass unit conversion
)
from .exceptions import (
    CalculatorError,            # base class for all package errors
    DivisionByZeroError,        # division/modulo by zero
    InvalidInputError,          # non-numeric input
    UnsupportedOperationError,  # unknown operation, unit, or category
    EmptyDataError,             # missing/empty dataset
)

# __all__ documents the public interface and controls what `from
# calculator_tools import *` exposes to callers.
__all__ = [
    "add",
    "subtract",
    "multiply",
    "divide",
    "percentage",
    "power",
    "modulo",
    "calculate",
    "average",
    "mean",
    "median",
    "total",
    "celsius_to_fahrenheit",
    "celsius_to_kelvin",
    "fahrenheit_to_celsius",
    "fahrenheit_to_kelvin",
    "kelvin_to_celsius",
    "kelvin_to_fahrenheit",
    "convert_temperature",
    "convert_unit",
    "CalculatorError",
    "DivisionByZeroError",
    "InvalidInputError",
    "UnsupportedOperationError",
    "EmptyDataError",
]
