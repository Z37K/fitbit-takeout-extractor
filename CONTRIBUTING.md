# Contributing to Fitbit Takeout Extractor

Thank you for considering contributing to Fitbit Takeout Extractor! This document outlines the process and guidelines for contributing to this project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YourUsername/fitbit-takeout-extractor.git
   cd fitbit-takeout-extractor
   ```
3. **Set up the development environment**:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Process

1. **Create a branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/my-new-feature
   ```
   or
   ```bash
   git checkout -b fix/my-bugfix
   ```

2. **Make your changes** and commit them with clear, descriptive messages:
   ```bash
   git commit -m "Add support for steps data"
   ```

3. **Push your branch** to your fork:
   ```bash
   git push origin feature/my-new-feature
   ```

4. **Create a Pull Request** from your fork to the main repository

## Coding Standards

- Follow PEP 8 style guidelines for Python code
- Add docstrings for all functions, classes, and modules
- Include type hints where appropriate
- Write tests for new features

## Adding a New Data Type Extractor

To add support for a new Fitbit data type:

1. Create a new file in `fitbit_extractor/extractors/` (e.g., `steps.py`)
2. Implement a class that handles the specific data type (see `heart_rate.py` as a template)
3. Update `fitbit_extractor/extractors/__init__.py` to expose your new extractor
4. Add a command-line interface in `command_line.py`
5. Add tests in the `tests/` directory
6. Update the README with information about the new data type

## Testing

Run tests using pytest:

```bash
pytest
```

## Documentation

- Update the README.md with any new features or changes
- Document your code with clear docstrings and comments

## Submitting a Pull Request

When you're ready to submit your changes:

1. Make sure all tests pass
2. Update documentation if necessary
3. Create a pull request with a clear description of the changes
4. Link any related issues in the pull request description

## Code of Conduct

Please be respectful and inclusive when contributing to this project. The goal is to create a welcoming and productive environment for everyone.
