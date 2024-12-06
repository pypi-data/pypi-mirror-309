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

