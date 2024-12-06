# Python Project Style Guide

This guide outlines our Python coding standards and best practices and out tooling and tech stack. 

## Tooling Overview

Our project relies on several powerful tools and libraries to ensure code quality, environment management, testing, automation, and more. Here’s an overview of each tool and how it contributes to a cleaner, more maintainable codebase.

### 1. `ruff` – Linting & Formatting

`ruff` is a powerful linter that implements the rule sets of multiple popular linters (e.g., flake8, pylint) and includes a robust set of formatters (e.g., Black, isort). It detects code smells, enforces style conventions, and performs refactor suggestions, helping us maintain consistent, clean code. `ruff` is also extremely fast—up to ten times faster than similar tools.

### 2. `uv` – Virtual Environment & Package Management

`uv` is a virtual environment and package manager that simplifies environment handling. Created by the developers behind `ruff`, it manages dependencies and Python versions efficiently, similar to `npm` for Node.js. With `uv`, setting up and switching between environments is seamless, which is crucial for consistent and reproducible development workflows.

### 3. `poethepoet` – Task Automation

`poethepoet` is our task automation tool, streamlining repetitive tasks (e.g., linting, testing, and building). It allows us to define custom tasks in the `pyproject.toml` file, making complex commands easier to run and document, thus improving project automation.

### 4. `pytest` – Testing Framework

`pytest` is our primary testing framework, known for its simplicity, flexibility, and powerful features like fixtures and parameterized testing. It helps us maintain robust, high-quality code by providing a structured environment for writing and running unit, integration, and end-to-end tests.

### 5. `rich` – CLI Framework & Logging Enhancements

`rich` is a CLI framework and rendering library for adding sophisticated visualizations to the terminal, including formatted logging, tracebacks, tables, and progress bars. It enhances user feedback and is valuable for both CLI apps and general debugging with clear, colorful output.

### 6. `loguru` – Logging Library

`loguru` is a modern, easy-to-use logging library with built-in support for formatting, rotating logs, and structured logging. It simplifies logging setup and enhances log readability, making debugging and monitoring easier and more efficient.

### 7. `pydantic` / `msgspec` – Data Validation & Serialization

Both `pydantic` and `msgspec` are powerful libraries for data validation and serialization. `pydantic` focuses on data modeling and type validation with support for complex data types, while `msgspec` offers efficient, fast serialization for both JSON and MsgPack formats. These libraries ensure data integrity and improve type safety across the application.

### 8. `litestar` / `fastapi` – Web Frameworks

`litestar` and `fastapi` are Python web frameworks with support for asynchronous programming, type annotations, and dependency injection. These frameworks enable us to build fast, high-performance APIs with clear structure and minimal boilerplate, supporting the development of scalable backend services.

### 9. `typer` / `click` – CLI Argument Parsing

`typer` and `click` are libraries for creating command-line interfaces. `typer` is built on top of `click` and uses Python type hints to create intuitive, type-safe CLIs. These tools make it easy to build complex CLI applications with features like auto-generated help messages and argument validation.


## Quickstart

1. Install `uv`:

    ```bash
    uv add --dev ruff
    ```

2. Copy the `pyproject.toml` and `.vscode` folder to your project root.

3. Run `uv sync` to sync to the `pyproject.toml`

You now have everything you need to get started!

Before we look into the tools let's discuss code style and naming conventions.

## Code Style Overview

We follow a pragmatic approach to Python development, emphasizing readability and maintainability while not being overly strict.

### Type Hints

Use type hints for function arguments and return values. They help catch errors early and serve as documentation:

```python
def calculate_total(prices: list[float], tax_rate: float) -> float:
    """Calculate total price including tax."""
    return sum(prices) * (1 + tax_rate)
```

### Docstrings (Google Style)

We use Google-style docstrings for documentation. Every function/class should have one:

```python
def transfer_funds(source: str, target: str, amount: float) -> bool:
    """Transfer funds between accounts.

    Longer description explaining complex behavior,
    edge cases, or important notes if needed.

    Args:
        source: Source account ID.
        target: Target account ID.
        amount: Amount to transfer.

    Returns:
        True if transfer was successful, False otherwise.

    Raises:
        InsufficientFunds: If source account lacks funds.
        AccountNotFound: If either account doesn't exist.
    """
```

For simple functions, a one-line docstring is sufficient:

```python
def is_valid_email(email: str) -> bool:
    """Check if the provided string is a valid email address."""
```

### Naming Conventions

- Classes: `PascalCase` (e.g., `BankAccount`)
- Functions/Variables: `snake_case` (e.g., `calculate_interest`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_ATTEMPTS`)
- Private attributes: prefix with underscore (e.g., `_internal_state`)

### Code Organization

1. Imports should be grouped and ordered:

   ```python
   # Standard library
   import os
   from typing import Optional

   # Third-party
   import pandas as pd
   import requests

   # Local
   from .utils import helper_function
   ```

2. Class organization:

   ```python
   class MyClass:
       """Class docstring."""

       def __init__(self):
           """Initialize the class."""
           pass

       # Public methods
       def public_method(self):
           pass

       # Private methods
       def _private_helper(self):
           pass
   ```

### Best Practices

1. **Explicit is Better Than Implicit**

   ```python
   # Good
   def process_data(data: list[dict], should_validate: bool = True):
       
   # Avoid
   def process_data(d, val=True):
   ```

2. **Use List/Dict Comprehensions When Clear**

   ```python
   # Good
   squares = [x * x for x in range(10)]

   # Avoid when complex
   matrix = [[i * j for i in range(10)] for j in range(10) if j % 2 == 0]
   ```

3. **Error Handling**

   ```python
   # Good
   try:
       result = perform_operation()
   except SpecificError as e:
       logger.error(f"Operation failed: {e}")
       raise
   ```

4. **Context Managers**

   ```python
   # Good
   with open('file.txt', 'r') as f:
       content = f.read()
   ```

5. **Default Arguments**

   ```python
   # Good
   def create_list(items: list[str] | None = None):
       items = items or []

   # Avoid
   def create_list(items: list[str] = []):  # Mutable default!
   ```


### Common Pitfalls to Avoid

1. **Mutable Default Arguments**

   ```python
   # Wrong
   def append_to(value, target=[]):
       target.append(value)
       return target

   # Right
   def append_to(value, target=None):
       if target is None:
           target = []
       target.append(value)
       return target
   ```

2. **Late Binding Closures**

   ```python
   # Wrong
   funcs = [lambda x: i * x for i in range(3)]

   # Right
   funcs = [lambda x, i=i: i * x for i in range(3)]
   ```

3. **Not Using Path Objects**

   ```python
   # Wrong
   file_path = base_dir + '/' + sub_dir + '/' + filename

   # Right
   from pathlib import Path
   file_path = Path(base_dir) / sub_dir / filename
   ```


By keeping these basic style guardrails in mind it will keep your code clean and maintanable without much effort!

### Tool Configuration Explained

Our `pyproject.toml` includes:

1. **Ruff Rules**:
   - `E`: Basic style errors (indentation, whitespace)
   - `F`: Logic errors (unused imports, undefined names)
   - `I`: Import sorting
   - `B`: Bug risk patterns
   - `C4`: Comprehension optimization
   - `UP`: Modern Python syntax
   - `N`: Naming conventions
   - `SIM`: Code simplification
   - `D`: Docstring style checks

2. **Pyright Settings**:
   - Basic type checking mode
   - Permissive with type inference
   - Doesn't require type stubs for all libraries


### VS Code Settings

Recommended VS Code settings (`settings.json`):

```json
{
    "python.analysis.typeCheckingMode": "basic",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.fixAll.ruff": true,
        "source.organizeImports.ruff": true
    }
}
```

### pyroject.toml - pyright settings

For more info -> 03_pyright

```toml

```

### pyroject.toml - ruff settings

```toml
# main settings
[tool.ruff]
# Enable a good set of rules that catch common issues
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort
    "D",   # pydocstyle
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "N",   # pep8-naming
    "SIM", # flake8-simplify
]
ignore = [
    "E501",  # Line length violations - let your editor handle wrapping
    "B006",  # Do not use mutable data structures for argument defaults
    "C901",  # Function is too complex
]
line-length = 100
# Exclude common directories
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
]

# Linting settings
[tool.ruff.lint]
pydocstyle.convention  = "google" # Use Google style docstrings

# Import organization
[tool.ruff.isort]
force-single-line = false
lines-after-imports = 2

[tool.ruff.mccabe]
# Maximum complexity allowed for functions
max-complexity = 12
```
