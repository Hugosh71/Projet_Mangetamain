Development Guide
=================

This guide provides information for developers who want to contribute to the Mangetamain project.

Getting Started with Development
================================

Prerequisites
-------------

Before starting development, ensure you have:

* Python 3.12+
* Poetry for dependency management
* Git for version control
* Docker (optional, for containerized development)

Development Setup
=================

1. **Clone the repository:**

.. code-block:: bash

   git clone https://github.com/Hugosh71/Projet_Mangetamain.git
   cd Projet_Mangetamain

2. **Set up the development environment:**

.. code-block:: bash

   poetry config virtualenvs.in-project true
   poetry env use python3.12
   poetry install --with dev

3. **Install pre-commit hooks:**

.. code-block:: bash

   poetry run pre-commit install

4. **Activate the virtual environment:**

.. code-block:: bash

   source .venv/bin/activate  # macOS/Linux
   .\.venv\Scripts\activate.ps1  # Windows

Project Structure
=================

The project follows a standard Python package structure:

.. code-block::

   mangetamain/
   ├── src/
   │   ├── app/           # Streamlit application
   │   │   └── main.py    # Main application entry point
   │   └── mangetamain/   # Core package
   │       ├── __init__.py
   │       └── core.py    # Core utilities and configuration
   ├── tests/             # Test suite
   │   ├── unit/          # Unit tests
   │   └── integration/   # Integration tests
   ├── docs/              # Documentation
   ├── notebooks/         # Jupyter notebooks
   ├── pyproject.toml     # Project configuration
   └── README.md

Code Style and Standards
========================

Code Formatting
---------------

The project uses several tools to maintain code quality:

* **Black**: Code formatting
* **Ruff**: Fast Python linter and formatter
* **Flake8**: Additional linting

Run formatting:

.. code-block:: bash

   make format

Run linting:

.. code-block:: bash

   make lint

Docstring Style
---------------

We use Google-style docstrings throughout the project. Example:

.. code-block:: python

   def example_function(param1: str, param2: int) -> bool:
       """Brief description of the function.

       More detailed description of what the function does and how it works.

       Args:
           param1 (str): Description of the first parameter.
           param2 (int): Description of the second parameter.

       Returns:
           bool: Description of the return value.

       Raises:
           ValueError: Description of when this exception is raised.

       Example:
           >>> result = example_function("hello", 42)
           >>> print(result)
           True
       """
       return True

Type Hints
----------

All functions and methods should include type hints:

.. code-block:: python

   from typing import List, Optional, Union

   def process_data(data: List[str],
                   filter_func: Optional[callable] = None) -> Union[List[str], None]:
       """Process a list of data items."""
       pass

Testing
=======

Test Structure
--------------

Tests are organized into two categories:

* **Unit tests** (`tests/unit/`): Test individual functions and classes
* **Integration tests** (`tests/integration/`): Test the application flow

Running Tests
-------------

Run all tests:

.. code-block:: bash

   make test

Run tests with coverage:

.. code-block:: bash

   poetry run pytest --cov=src --cov-report=html

Run specific test files:

.. code-block:: bash

   poetry run pytest tests/unit/test_core.py

Writing Tests
-------------

Follow these guidelines when writing tests:

1. **Test naming**: Use descriptive test names that explain what is being tested
2. **Test structure**: Follow the Arrange-Act-Assert pattern
3. **Test isolation**: Each test should be independent
4. **Test coverage**: Aim for high test coverage (90%+)

Example test:

.. code-block:: python

   def test_get_app_config_returns_defaults():
       """Test that get_app_config returns default configuration values."""
       # Arrange
       expected_name = "Mangetamain"
       expected_version = "0.1.0"

       # Act
       config = get_app_config()

       # Assert
       assert isinstance(config, AppConfig)
       assert config.name == expected_name
       assert config.version == expected_version

Docker Development
==================

Using Docker for development provides a consistent environment:

**Build the development image:**

.. code-block:: bash

   docker build -f Dockerfile -t mangetamain:dev .

**Run the application:**

.. code-block:: bash

   docker run --rm -it -p 8501:8501 mangetamain:dev

**Run tests in Docker:**

.. code-block:: bash

   docker compose run --rm tests

**Run linting in Docker:**

.. code-block:: bash

   docker compose run --rm lint

Git Workflow
============

Branching Strategy
------------------

* **main**: Production-ready code
* **develop**: Integration branch for features
* **feature/***: Feature development branches
* **hotfix/***: Critical bug fixes

Commit Guidelines
-----------------

Use conventional commit messages:

.. code-block:: bash

   feat: add new data visualization feature
   fix: resolve memory leak in data processing
   docs: update installation guide
   test: add unit tests for core module
   refactor: improve code organization

Pull Request Process
--------------------

1. **Create a feature branch:**

.. code-block:: bash

   git checkout -b feature/new-feature

2. **Make your changes and commit:**

.. code-block:: bash

   git add .
   git commit -m "feat: add new feature"

3. **Push the branch:**

.. code-block:: bash

   git push origin feature/new-feature

4. **Create a pull request** with:
   * Clear description of changes
   * Reference to related issues
   * Screenshots for UI changes
   * Test results

Code Review Guidelines
======================

When reviewing code, check for:

* **Functionality**: Does the code work as intended?
* **Style**: Does it follow the project's style guidelines?
* **Documentation**: Are docstrings and comments adequate?
* **Tests**: Are there appropriate tests?
* **Performance**: Are there any performance concerns?
* **Security**: Are there any security issues?

Documentation
=============

Documentation is built using Sphinx and is located in the `docs/` directory.

**Build documentation:**

.. code-block:: bash

   cd docs
   sphinx-build -b html . _build/html

**View documentation:**

Open `docs/_build/html/index.html` in your browser.

**Update documentation:**

When adding new features, update the relevant documentation files:

* API documentation in `docs/api/`
* Usage examples in `docs/usage.rst`
* Installation instructions in `docs/installation.rst`

Release Process
==============

Versioning
----------

We use semantic versioning (MAJOR.MINOR.PATCH):

* **MAJOR**: Breaking changes
* **MINOR**: New features (backward compatible)
* **PATCH**: Bug fixes (backward compatible)

Release Steps
-------------

1. **Update version** in `pyproject.toml`
2. **Update changelog** with new features and fixes
3. **Create release tag:**

.. code-block:: bash

   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0

4. **Build and publish** the package

Troubleshooting
===============

Common Development Issues
------------------------

**Import errors:**

.. code-block:: bash

   # Ensure the package is installed in development mode
   poetry install

**Test failures:**

.. code-block:: bash

   # Clear Python cache
   find . -type d -name "__pycache__" -delete
   find . -type f -name "*.pyc" -delete

**Docker issues:**

.. code-block:: bash

   # Rebuild the Docker image
   docker build --no-cache -t mangetamain:dev .

**Pre-commit hook failures:**

.. code-block:: bash

   # Run pre-commit on all files
   poetry run pre-commit run --all-files

Getting Help
============

If you need help with development:

1. **Check the documentation**: Review this guide and API docs
2. **Search issues**: Look for similar issues on GitHub
3. **Ask questions**: Create a new issue with the "question" label
4. **Join discussions**: Participate in project discussions

Contributing
============

We welcome contributions! Please see the :doc:`contributing` guide for detailed information on how to contribute to the project.
