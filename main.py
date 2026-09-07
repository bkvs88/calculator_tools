"""main.py — Interactive demo and usage example for calculator_tools.

Run this file directly (``python3 main.py``) to see every feature of the
package in action, including basic arithmetic, statistics, temperature and
unit conversions, and package error handling.
"""

import os  # standard library: filesystem paths
import sys # standard library: interpreter/runtime access

# Add the parent directory of this file to sys.path so the
# ``calculator_tools`` package (one level up from main.py) is importable
# even when this file is run directly as a script rather than from a
# package context.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the public API from the ``calculator_tools`` package.
from calculator_tools import (
    add,                        # a + b
    subtract,                   # a - b
    multiply,                   # a * b
    divide,                     # a / b
    percentage,                 # part as a % of whole
    power,                      # base ** exponent
    average,                    # arithmetic mean of data
    median,                     # middle value of data
    convert_temperature,        # convert C/F/K temperatures
    convert_unit,               # convert length/mass units
    DivisionByZeroError,        # divide/modulo by zero
    InvalidInputError,          # non-numeric input
    UnsupportedOperationError,  # unknown operation/unit
    EmptyDataError,             # empty/missing dataset
)


def demo():
    """Run a series of examples demonstrating the package's features."""
    print("=== Basic arithmetic ===")
    print("10 + 5      =", add(10, 5))
    print("10 - 5      =", subtract(10, 5))
    print("10 * 5      =", multiply(10, 5))
    print("10 / 5      =", divide(10, 5))
    print("10 % 50     =", percentage(10, 50))
    print("2 ** 8      =", power(2, 8))

    print("\n=== Statistics ===")
    data = [10, 20, 30, 40, 50]
    print("average     =", average(data))
    print("median      =", median(data))

    print("\n=== Temperature conversion ===")
    print("100 C in F  =", convert_temperature(100, "C", "F"))
    print("32 F in C   =", convert_temperature(32, "F", "C"))
    print("0 C in K    =", convert_temperature(0, "C", "K"))

    print("\n=== Unit conversion ===")
    print("1 mile -> km =", convert_unit(1, "mi", "km", "length"))
    print("1 kg -> lb   =", convert_unit(1, "kg", "lb", "mass"))

    print("\n=== Error handling ===")
    # Try several invalid calls and confirm each raises the right error.
    for label, func in [
        ("divide by zero", lambda: divide(5, 0)),
        ("non-numeric", lambda: add("a", 1)),
        ("unsupported op", lambda: convert_unit(1, "parsec", "km", "length")),
        ("empty data", lambda: average([])),
    ]:
        try:
            func()
            # If we reach here, the call unexpectedly did not raise.
            print(f"{label:<20} -> no error (unexpected!)")
        except (DivisionByZeroError, InvalidInputError, UnsupportedOperationError, EmptyDataError) as e:
            print(f"{label:<20} -> {type(e).__name__}: {e}")


if __name__ == "__main__":
    # Only run the demo when this file is executed directly, not when it
    # is imported as a module.
    demo()
