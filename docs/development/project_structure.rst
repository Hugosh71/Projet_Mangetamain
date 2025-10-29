
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
