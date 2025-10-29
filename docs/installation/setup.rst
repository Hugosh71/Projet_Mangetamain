
Environment Setup
=================

Method 1: Using Poetry (Recommended)
------------------------------------

This is the recommended method for development and local usage.

1. **Clone the repository:**

.. code-block:: bash

   git clone https://github.com/Hugosh71/Projet_Mangetamain.git
   cd Projet_Mangetamain

2. **Configure Poetry to create virtual environments in the project:**

.. code-block:: bash

   poetry config virtualenvs.in-project true
   poetry env use python3.12

3. **Install dependencies:**

.. code-block:: bash

   poetry install

Install additional development dependencies:

.. code-block:: bash

   poetry install --with dev
   poetry run pre-commit install

This will install:

* Testing tools (pytest, pytest-cov)
* Code formatting (black, ruff)
* Linting (flake8, ruff)
* Pre-commit hooks

4. **Activate the virtual environment:**

   **Option A: Using VS Code**

   - Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
   - Type "Python: Select Interpreter"
   - Select the mangetamain environment

   **Option B: Using terminal**

   Windows:

   .. code-block:: bash

      .\.venv\Scripts\activate.ps1

   macOS/Linux:

   .. code-block:: bash

      source .venv/bin/activate

5. **Run the application:**

.. code-block:: bash

   poetry run streamlit run src/app/main.py --server.port=8501 --server.address=0.0.0.0

Method 2: Using Docker
----------------------

For containerized deployment:

1. **Clone the repository:**

.. code-block:: bash

   git clone https://github.com/Hugosh71/Projet_Mangetamain.git
   cd Projet_Mangetamain

2. **Build the Docker image:**

.. code-block:: bash

   docker build -t mangetamain:latest .

3. **Run the container:**

.. code-block:: bash

   docker run --rm -it -p 8501:8501 mangetamain:latest

Method 3: Using Docker Compose
------------------------------

For development with all services:

1. **Clone the repository:**

.. code-block:: bash

   git clone https://github.com/Hugosh71/Projet_Mangetamain.git
   cd Projet_Mangetamain

2. **Run with Docker Compose:**

.. code-block:: bash

   docker compose up app

Verification
------------

After installation, verify that everything is working correctly:

1. **Check Python version:**

.. code-block:: bash

   python --version

2. **Check Poetry installation:**

.. code-block:: bash

   poetry --version

3. **Check dependencies:**

.. code-block:: bash

   poetry show

4. **Run tests:**

.. code-block:: bash

   make test

5. **Access the application:**

   Open your browser and navigate to `http://localhost:8501`

Troubleshooting
---------------

Common Issues

**Issue: Python version mismatch**

.. code-block:: bash

   # Solution: Use the correct Python version
   poetry env use python3.12

**Issue: Virtual environment not activated**

.. code-block:: bash

   # Solution: Activate the virtual environment
   source .venv/bin/activate  # macOS/Linux
   .\.venv\Scripts\activate.ps1  # Windows

**Issue: Dependencies not installed**

.. code-block:: bash

   # Solution: Reinstall dependencies
   poetry install

**Issue: Port already in use**

.. code-block:: bash

   # Solution: Use a different port
   poetry run streamlit run src/app/main.py --server.port=8502

Next Steps
----------

After successful installation, you can:

1. Read the :doc:`../usage/index` guide to learn how to use the application
2. Explore the :doc:`../api/index` for detailed API documentation
3. Check the :doc:`../development/index` guide for contributing to the project
