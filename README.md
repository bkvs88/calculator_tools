# calculator_tools

A small Python package demonstrating the difference between **functions**,
**modules**, **packages**, **imports**, and **exception handling** — using
itself as a live example.

```
calculator_tools/
├── __init__.py      <- package marker + public API re-exports
├── arithmetic.py    <- module: basic math
├── statistics.py    <- module: statistics
├── converter.py     <- module: temperature/unit conversion
├── exceptions.py    <- module: custom error types
└── main.py          <- module: runnable demo
```

---

## 1. Function

A **function** is a named block of reusable code that performs one task and
returns a result. You define it once and call it many times.

```python
>>> from calculator_tools import add
>>> add(10, 5)
15
```

Here `add` is a function. It is defined in `arithmetic.py`, validates its
inputs with `_validate_number`, and returns `a + b`.

**Key traits**

- Callable: `add(10, 5)`
- Takes arguments: `a`, `b`
- Returns a result: `15`
- Has one clear job: sum two numbers

Other functions in this package: `subtract`, `divide`, `average`, `median`,
`convert_temperature`, `convert_unit`, `percentage`, `power`, `modulo`,
`calculate`.

---

## 2. Module

A **module** is a single `.py` file that groups related functions, classes,
and variables together. It's one way to organise code by purpose.

| Module file    | What it groups                                    |
| -------------- | ------------------------------------------------- |
| `arithmetic.py` | `add`, `subtract`, `multiply`, `divide`, ...      |
| `statistics.py` | `average`, `mean`, `median`, `total`              |
| `converter.py`  | `convert_temperature`, `convert_unit`, ...        |
| `exceptions.py` | `CalculatorError`, `DivisionByZeroError`, ...     |

**Function vs. module**

```python
# One function lives in one module.
#   arithmetic.py
def add(a, b):
    return a + b
```

- A function is a single unit of behaviour.
- A module is a file that can contain many functions plus their helpers
  (such as `_validate_number` in `arithmetic.py`) and shared state.

---

## 3. Package

A **package** is a directory of modules that Python treats as a single
namespace, marked by an `__init__.py` file. It lets you organise related
modules into one importable name.

```python
calculator_tools/        <- the package
├── __init__.py          <- makes the folder a package
├── arithmetic.py        <- submodule
├── statistics.py        <- submodule
└── ...
```

The `__init__.py` in this project does two things:

1. Re-exports the public API so users write one short import instead of
   reaching into each file:

   ```python
   # inside __init__.py
   from .arithmetic import add, subtract, multiply, divide, ...
   ```

2. Defines `__all__`, which controls what `from calculator_tools import *`
   exposes.

**Module vs. package**

```python
arithmetic.py          # a module (one file)
calculator_tools/      # a package (a folder of modules)
```

---

## 4. Import

An **import** is a statement that loads code from another module or package
so you can reuse it. There are three common styles, and this project uses
all of them.

### 4a. Standard library import

`main.py` line 8:

```python
import os
import sys
```

Loads Python's built-in modules for filesystem paths and runtime access.
They are used in `main.py:15` to make the package importable when the file
runs directly as a script.

### 4b. Package import (absolute)

`main.py` line 18:

```python
from calculator_tools import add, subtract, multiply, divide
```

`calculator_tools` is the package name, `add` is the function we want. This
works because `__init__.py` re-exported `add`, so we don't need to know that
it actually lives in `arithmetic.py`.

### 4c. Relative import

`arithmetic.py` line 7:

```python
from .exceptions import DivisionByZeroError, InvalidInputError
```

The leading `.` means "the current package". So this says: inside
`calculator_tools`, load `DivisionByZeroError` from the sibling module
`exceptions.py`. Relative imports only make sense inside a package.

---

## 5. Exception handling

Exceptions are how Python reports **errors at runtime** instead of crashing
silently or returning bad results. A function detects a problem and
`raise`s an exception; the caller intercepts it with `try/except` and
decides what to do.

### 5a. Raising an exception

When a function cannot do its job, it stops and `raise`s an exception —
`arithmetic.py` line 57:

```python
if b == 0:
    raise DivisionByZeroError("Cannot divide by zero")
```

The message is optional but useful: it becomes part of the display and can
be read from `exc.args[0]` or the exception's `str()`.

### 5b. Catching an exception

`main.py` lines 60-73 wraps each risky call in `try/except`:

```python
try:
    func()
except (DivisionByZeroError, InvalidInputError,
        UnsupportedOperationError, EmptyDataError) as e:
    print(f"{label:<20} -> {type(e).__name__}: {e}")
```

The full `try` statement anatomy:

```
try:        # run code that might fail
    ...
except SomeError:    # handle one specific error
    ...
except Exception:    # catch-all for anything else (use sparingly)
    ...
else:       # runs only if no exception was raised
    ...
finally:    # always runs, even on errors (cleanup)
    ...
```

### 5c. Structural definition — the exception hierarchy

All exceptions are **classes**. A custom exception is a class that inherits
from `Exception` (directly or indirectly). Here is the whole hierarchy from
`exceptions.py`:

```
       BaseException          (Python built-in)
              │
           Exception          (Python built-in — inherit from this)
              │
     CalculatorError          (our package base class)
          │  │  │  │
          │  │  │  └── EmptyDataError
          │  │  └────── UnsupportedOperationError
          │  └────────── InvalidInputError
          └────────────── DivisionByZeroError
```

```python
# exceptions.py
class CalculatorError(Exception):
    """Base exception for the calculator_tools package."""


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""


class InvalidInputError(CalculatorError):
    """Raised when input is not a valid number (e.g. a string or bool)."""
```

**Structural definition** means: describe what makes the exception distinct
through *inheritance*, not duplicated code. Every child reuses
`CalculatorError`'s behaviour as its parent — so one `except CalculatorError`
catches *every* package error, while a caller can still catch a specific
type like `DivisionByZeroError` first.

### 5d. Core components of a custom exception

A fully-featured custom exception is built from these parts:

| # | Component      | Purpose                                                      |
| - | -------------- | ------------------------------------------------------------ |
| 1 | **Class name** | Descriptive, usually ends in `Error` (`InvalidInputError`).  |
| 2 | **Parent**     | `Exception`, or a package base like `CalculatorError`.       |
| 3 | **Docstring**  | Explains *when* the exception is raised.                     |
| 4 | `__init__`     | Optional constructor; runs when the exception is created.    |
| 5 | **Attributes** | Extra data stored on the instance (`self.message`, `self.value`). |
| 6 | `super().__init__` | Must be called so the exception message is forwarded up.  |
| 7 | `__str__`      | Optional; controls the human-readable message.               |

An example combining all of them:

```python
class UnsupportedFileError(CalculatorError):        # (1) name + (2) parent
    """Raised when a file extension is not recognised."""  # (3) docstring

    def __init__(self, filename, extension):        # (4) constructor
        self.filename = filename                    # (5) attributes
        self.extension = extension
        super().__init__(                           # (6) forward to parent
            f"Unsupported file '{filename}' (extension '{extension}')"
        )

    def __str__(self):                              # (7) display form
        return self.message
```

The examples in `exceptions.py` use the minimal form (components 1-3 only)
because they need no extra data. Add components 4-7 when your exception must
carry context — for example the offending `filename` — so the caller can
inspect it after catching the exception:

```python
from calculator_tools import DivisionByZeroError

try:
    divide(5, 0)
except DivisionByZeroError as err:   # narrowest catch first
    print(type(err).__name__, err)   # the str() of the exception
except CalculatorError as err:       # any other package error
    print("package error:", err)
```

---

## Putting it all together

The hierarchy builds bottom-up:

```
          IMPORT
             |
          PACKAGE  (calculator_tools/  +  __init__.py)
         /    |    \
    MODULE  MODULE  MODULE      (arithmetic.py, statistics.py, ...)
      |       |       |
  FUNCTION FUNCTION FUNCTION     (add, average, convert_unit, ...)
```

A working example of every level:

```python
# 1. Import the package's re-exported functions.
from calculator_tools import add, average, convert_temperature

# 2. Call functions (defined inside modules).
total = add(10, 5)                          # function
avg   = average([10, 20, 30])               # function
print(convert_temperature(100, "C", "F"))   # function

print("package =", __import__("calculator_tools").__name__)
```

## Quick start

```bash
python3 main.py
```

runs the interactive demo showing arithmetic, statistics, conversions, and
error handling.