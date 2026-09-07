"""converter.py — Temperature and physical unit conversions.

Includes direct Celsius/Fahrenheit/Kelvin helpers, a generic
``convert_temperature`` dispatcher, and a ``convert_unit`` function for
length and mass units.
"""

from .exceptions import (
    InvalidInputError,          # raised for invalid numbers
    UnsupportedOperationError,  # raised for unknown units/categories
)


def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit using F = (C * 9/5) + 32."""
    _validate_number(celsius, "celsius")
    return (celsius * 9 / 5) + 32


def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin (K = C + 273.15).

    Raises:
        InvalidInputError: if the temperature is below absolute zero.
    """
    _validate_number(celsius, "celsius")
    if celsius < -273.15:
        raise InvalidInputError("Temperature cannot be below absolute zero")
    return celsius + 273.15


def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius using C = (F - 32) * 5/9."""
    _validate_number(fahrenheit, "fahrenheit")
    return (fahrenheit - 32) * 5 / 9


def fahrenheit_to_kelvin(fahrenheit):
    """Convert Fahrenheit to Kelvin by routing through Celsius."""
    return celsius_to_kelvin(fahrenheit_to_celsius(fahrenheit))


def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius (C = K - 273.15).

    Raises:
        InvalidInputError: if the temperature is below absolute zero.
    """
    _validate_number(kelvin, "kelvin")
    if kelvin < 0:
        raise InvalidInputError("Temperature cannot be below absolute zero")
    return kelvin - 273.15


def kelvin_to_fahrenheit(kelvin):
    """Convert Kelvin to Fahrenheit by routing through Celsius."""
    return celsius_to_fahrenheit(kelvin_to_celsius(kelvin))


def convert_temperature(value, from_unit, to_unit):
    """Convert a temperature between Celsius, Fahrenheit, or Kelvin.

    Accepts unit names/symbols: "c"/"celsius", "f"/"fahrenheit",
    "k"/"kelvin". Conversion is always routed through Celsius.
    """
    value = _validate_number(value, "value")
    # Normalize unit strings: trim whitespace and lowercase them.
    from_unit = str(from_unit).strip().lower()
    to_unit = str(to_unit).strip().lower()

    # Map accepted symbols/names to a single canonical name.
    canonical = {
        "c": "celsius",
        "celsius": "celsius",
        "f": "fahrenheit",
        "fahrenheit": "fahrenheit",
        "k": "kelvin",
        "kelvin": "kelvin",
    }

    src = canonical.get(from_unit)
    dst = canonical.get(to_unit)
    if not src:
        raise UnsupportedOperationError(f"Unsupported temperature unit: {from_unit}")
    if not dst:
        raise UnsupportedOperationError(f"Unsupported temperature unit: {to_unit}")

    # Convert the source unit to Celsius, then from Celsius to the target.
    to_celsius = {
        "celsius": lambda v: v,
        "fahrenheit": fahrenheit_to_celsius,
        "kelvin": kelvin_to_celsius,
    }
    from_celsius = {
        "celsius": lambda v: v,
        "fahrenheit": celsius_to_fahrenheit,
        "kelvin": celsius_to_kelvin,
    }

    celsius = to_celsius[src](value)
    return from_celsius[dst](celsius)


# Length conversion factors expressed relative to meters (1 unit = N meters).
_LENGTH_UNITS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.344,
}

# Mass conversion factors expressed relative to kilograms (1 unit = N kg).
_MASS_UNITS = {
    "mg": 0.000001,
    "g": 0.001,
    "kg": 1.0,
    "t": 1000.0,
    "oz": 0.028349523125,
    "lb": 0.45359237,
}

# Group the unit tables by conversion category.
_CATEGORY_FACTORS = {
    "length": _LENGTH_UNITS,
    "mass": _MASS_UNITS,
}


def convert_unit(value, from_unit, to_unit, category):
    """Convert ``value`` between units within a given category.

    Categories: "length" or "mass". Conversion is done by dividing both
    unit factors by their base (meter/kilogram) so any two units combine.

    Example: convert_unit(1, "mi", "km", "length") -> 1.609344
    """
    value = _validate_number(value, "value")
    category = str(category).strip().lower()
    if category not in _CATEGORY_FACTORS:
        raise UnsupportedOperationError(f"Unsupported conversion category: {category}")

    table = _CATEGORY_FACTORS[category]
    from_key = str(from_unit).strip().lower()
    to_key = str(to_unit).strip().lower()
    if from_key not in table:
        raise UnsupportedOperationError(f"Unsupported {category} unit: {from_unit}")
    if to_key not in table:
        raise UnsupportedOperationError(f"Unsupported {category} unit: {to_unit}")

    # value * (from factor) / (to factor) gives the converted amount.
    return value * table[from_key] / table[to_key]


def _validate_number(value, name="value"):
    """Ensure ``value`` is a real number and return it unchanged.

    Raises:
        InvalidInputError: if ``value`` is a bool or a non-number.
    """
    # bool is a subclass of int, so reject it explicitly.
    if isinstance(value, bool):
        raise InvalidInputError(f"{name} must be a number, got bool")
    if not isinstance(value, (int, float)):
        raise InvalidInputError(f"{name} must be a number, got {type(value).__name__}")
    return value
