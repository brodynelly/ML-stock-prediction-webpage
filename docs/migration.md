# Migration Guide

This document details the changes made during the refactoring process to improve code quality, maintainability, and testability.

## Changes

### Directory Structure

The repository structure has been reorganized to follow standard Python project conventions:

- Moved source code to `src/stock_forecasting/`.
- Created a `tests/` directory for unit tests.
- Added `pyproject.toml` for configuration and dependency management.
- Added `.github/workflows/ci.yml` for Continuous Integration.

### Code Refactoring

- **Modularity**: The monolithic `main.py` script has been split into `app.py` (UI logic) and `utils.py` (core logic).
- **Functions**: Core logic (data loading, model training, forecasting) is now encapsulated in pure functions in `utils.py`.
- **Type Hinting**: Added type hints to all functions for better code clarity and static analysis.
- **Error Handling**: Improved error handling and logging in data loading functions.
- **Logging**: Replaced print statements with standard Python logging.

### Tooling

- **Dependency Management**: Moved from `requirements.txt` to `pyproject.toml`.
- **Linting & Formatting**: Integrated `ruff` for fast linting and formatting.
- **Testing**: Added `pytest` for unit testing.
- **Type Checking**: Added `mypy` for static type checking.
- **CI/CD**: Added GitHub Actions workflow to run tests, linting, and type checking on every push and PR.

## How to Adapt

If you have a local copy of the repository:

1.  Pull the latest changes.
2.  Re-install dependencies: `pip install -e .[dev]`.
3.  Run the app using the new path: `streamlit run src/stock_forecasting/app.py`.
