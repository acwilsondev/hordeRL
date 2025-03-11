# Contributing to HordeRL

Thank you for considering contributing to HordeRL! This document provides guidelines and instructions to help you get started with development.

## Development Setup

### Prerequisites

- Python 3.8 or newer
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management

### Setting Up Your Development Environment

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/hordeRL.git
   cd hordeRL
   ```

2. **Install dependencies with Poetry**

   ```bash
   poetry install
   ```

   This will create a virtual environment and install all required dependencies, including development dependencies.

3. **Activate the virtual environment**

   ```bash
   poetry shell
   ```

4. **Run the game in development mode**

   ```bash
   python hordeRL.py --log DEBUG --terminal_log
   ```

### Development Dependencies

The project includes several development dependencies:
- Testing tools (pytest)
- Linting and code quality tools
- Debugging utilities

You can install all development dependencies using Poetry:

```bash
poetry install --with dev
```

## Code Style Guidelines

We follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code with some specific additions:

1. **Line Length**: Keep lines to a maximum of 88 characters (compatible with Black formatter)
2. **Docstrings**: Use Google-style docstrings for all public functions, classes, and methods
3. **Type Hints**: Include type hints for all function parameters and return values
4. **Comments**: Write clear, concise comments for complex logic
5. **Naming Conventions**:
   - Use `snake_case` for variables and functions
   - Use `PascalCase` for classes
   - Use `UPPER_CASE` for constants

### Code Formatting

We use the following tools for code quality:
- [Black](https://black.readthedocs.io/en/stable/) for code formatting
- [isort](https://pycqa.github.io/isort/) for import sorting
- [flake8](https://flake8.pycqa.org/en/latest/) for linting

Run these tools before submitting changes:

```bash
poetry run black .
poetry run isort .
poetry run flake8
```

## How to Submit Changes

1. **Create a new branch** for your changes:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and commit them with clear, descriptive commit messages:

   ```bash
   git commit -m "Add feature: description of the feature"
   ```

3. **Run tests** to ensure your changes don't break existing functionality:

   ```bash
   poetry run pytest
   ```

4. **Push your branch** to your fork:

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** against the main repository's main branch
   - Include a clear description of the changes
   - Reference any related issues
   - Explain how to test your changes

6. **Address review feedback** and make any requested changes
   
7. Once approved, your changes will be merged

## Development Workflow

### Issue Tracking

- Check the [Issues](https://github.com/your-organization/hordeRL/issues) page for tasks that need attention
- Comment on an issue if you plan to work on it
- Create new issues for bugs or feature requests you discover

### Branching Strategy

- `main` branch contains stable, released code
- `develop` branch is for ongoing development
- Feature branches should be created from `develop` and named according to the feature they implement
- Hotfix branches should be created from `main` for urgent fixes

### Testing

Write tests for all new features and bug fixes. Run the test suite before submitting your changes:

```bash
poetry run pytest
```

### Debugging

The game supports various debugging flags:

```bash
python hordeRL.py --log DEBUG --terminal_log --prof
```

- `--log` sets the logging level (DEBUG, INFO, WARNING, ERROR)
- `--terminal_log` outputs logs to the terminal
- `--prof` enables profiling to identify performance bottlenecks

## Release Process

1. Update version numbers in `pyproject.toml`
2. Update the changelog
3. Create a pull request to merge changes into the main branch
4. Once merged, create a new release tag

Thank you for contributing to HordeRL!

