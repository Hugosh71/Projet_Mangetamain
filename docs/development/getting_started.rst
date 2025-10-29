
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
-----------------

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
