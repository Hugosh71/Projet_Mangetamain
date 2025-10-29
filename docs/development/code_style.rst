
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
-------

**Test Structure**

Tests are organized into two categories:

* **Unit tests** (`tests/unit/`): Test individual functions and classes
* **Integration tests** (`tests/integration/`): Test the application flow

**Running Tests**

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
