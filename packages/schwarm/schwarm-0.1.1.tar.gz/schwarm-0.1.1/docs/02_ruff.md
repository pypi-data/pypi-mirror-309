# Ruff Configuration Guide

This guide explains our Ruff configuration in detail, showing what each rule does, why we chose it, and examples of what it catches.

## Our Configuration

```toml
[tool.ruff]
# Rule selection
select = ["E", "F", "I", "B", "C4", "UP", "N", "SIM", "D"]
ignore = ["E501", "B006", "C901"]
line-length = 100

# Additional settings
target-version = "py38"
fix = true
ignore-init-module-imports = true
respect-gitignore = true
show-fixes = true
cache-dir = ".ruff_cache"

[tool.ruff.pydocstyle]
convention = "google"
```

## Rule Sets Explained

### E - pycodestyle Errors

Basic Python style enforcement.

```python
# E201 - Whitespace after '('
# Bad
function( argument)
# Good
function(argument)

# E225 - Missing whitespace around operator
# Bad
x=1
# Good
x = 1

# E271 - Multiple spaces after keyword
# Bad
if   x == 1:
# Good
if x == 1:
```

### F - Pyflakes

Logical and runtime error detection.

```python
# F401 - Unused imports
# Bad
import sys  # Never used
x = 1

# F821 - Undefined name
# Bad
x = undefined_variable

# F841 - Unused variable
# Bad
def func():
    x = 1  # Never used
    return 2
```

### I - isort

Import organization and sorting.

```python
# Bad
import sys
import os
import pandas as pd
from mymodule import thing
from typing import List

# Good
from typing import List

import os
import sys

import pandas as pd

from mymodule import thing
```

### B - flake8-bugbear

Catches bug risks and code patterns that might indicate errors.

```python
# B007 - Loop variable overwritten
# Bad
for x in range(10):
    pass
x = 1  # Overshadows loop variable

# B904 - Within an except clause, raise exceptions with raise ... from err
# Bad
try:
    do_something()
except Exception as e:
    raise ValueError("Failed")
# Good
try:
    do_something()
except Exception as e:
    raise ValueError("Failed") from e

# B010 - Do not call setattr with a constant attribute value
# Bad
setattr(self, "name", "value")
# Good
self.name = "value"
```

### C4 - flake8-comprehensions

Optimizes comprehension patterns and makes them more Pythonic.

```python
# C400 - Unnecessary generator - use list comprehension
# Bad
list(x for x in range(10))
# Good
[x for x in range(10)]

# C401 - Unnecessary generator - use set comprehension
# Bad
set(x for x in range(10))
# Good
{x for x in range(10)}

# C402 - Unnecessary generator - use dict comprehension
# Bad
dict((x, x) for x in range(10))
# Good
{x: x for x in range(10)}
```

### UP - pyupgrade

Modernizes Python code syntax.

```python
# UP001 - Use dict union operator
# Bad (Python 3.8+)
{**x, **y}
# Good
x | y

# UP007 - Use X | Y for type unions
# Bad
from typing import Union
x: Union[int, str]
# Good
x: int | str

# UP015 - Unnecessary open mode "b"
# Bad
open("file", "rb").read().decode()
# Good
open("file", "r", encoding="utf-8").read()
```

### N - pep8-naming

Enforces Python naming conventions.

```python
# N801 - Class name should use CapWords
# Bad
class my_class:
# Good
class MyClass:

# N802 - Function name should be lowercase
# Bad
def MyFunction():
# Good
def my_function():

# N803 - Argument name should be lowercase
# Bad
def function(BadName):
# Good
def function(good_name):
```

### SIM - flake8-simplify

Suggests simpler code alternatives.

```python
# SIM101 - Multiple isinstance calls
# Bad
if isinstance(x, int) or isinstance(x, float):
# Good
if isinstance(x, (int, float)):

# SIM108 - Use ternary operator
# Bad
if condition:
    x = 1
else:
    x = 2
# Good
x = 1 if condition else 2

# SIM401 - Use dict.get
# Bad
value = my_dict[key] if key in my_dict else default
# Good
value = my_dict.get(key, default)
```

### D - pydocstyle (Google Convention)

Enforces consistent documentation style.

```python
# D100-D103 - Missing docstring
# Bad
def function(x):
    pass

# Good
def function(x):
    """Do something with x."""
    pass

# D201 - No blank lines after function docstring
# Bad
def function():
    """Do something.
    
    """
    pass

# Good
def function():
    """Do something."""
    pass

# D300 - Use triple double quotes
# Bad
def function():
    '''Do something.'''
    
# Good
def function():
    """Do something."""
```

## Ignored Rules Explained

### E501 - Line Length

```python
# We ignore this because:
# 1. Modern editors wrap lines
# 2. Some lines (URLs, long strings) are better long
# 3. We set line-length = 100 as a guideline, not strict rule

# This is fine in our config:
def function_with_a_very_long_name(parameter_one: str, parameter_two: str, parameter_three: str = "default_value"):
    pass
```

### B006 - Mutable Default Arguments

```python
# We ignore this because when used carefully, mutable defaults can be useful
# Just document when you use them!

# This is allowed in our config:
def append_to_history(item: str, history: list = []):
    """Append to history list.
    
    Note: Uses mutable default intentionally to maintain history.
    """
    history.append(item)
    return history
```

### C901 - Complex Function

```python
# We ignore this because:
# 1. Sometimes complexity is necessary
# 2. Breaking up functions can make code harder to follow
# 3. Better to focus on readability than arbitrary metrics

# This is allowed in our config:
def process_data(data: dict) -> dict:
    if condition1:
        if condition2:
            for item in data:
                if condition3:
                    # Complex but clear processing
                    pass
    return data
```

## Additional Settings Explained

```toml
target-version = "py38"  # Enables Python 3.8+ syntax features
fix = true              # Automatically fix what can be fixed
respect-gitignore = true  # Don't check files in .gitignore
show-fixes = true       # Show what was automatically fixed
```

## Common Workflows

### 1. Check Single File

```bash
ruff check file.py
```

### 2. Fix All Issues

```bash
ruff check --fix .
```

### 3. Show All Rules

```bash
ruff rule 'E***'  # Shows all pycodestyle rules
```

### 4. Format Imports Only

```bash
ruff check --select I --fix .
```

## VS Code Integration

```json
{
    "editor.codeActionsOnSave": {
        "source.fixAll.ruff": true,
        "source.organizeImports.ruff": true
    }
}
```

## Git Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.3
    hooks:
    -   id: ruff
        args: [--fix]
```

## When to Disable Rules

Sometimes it makes sense to disable rules for specific lines. Use comments like:

```python
# For a single line:
x = 1  # noqa: E402

# For a block of code:
# ruff: noqa: E402, E501
def some_function():
    pass

# To disable specific rules for the whole file:
"""Module docstring."""
# ruff: noqa: D100, D101, D102
```

Remember: The goal of these rules is to help write better code, not to make coding harder. If a rule is consistently getting in your way, we can discuss adjusting the configuration.
