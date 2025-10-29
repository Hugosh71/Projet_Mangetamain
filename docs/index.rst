Welcome to Mangetamain's documentation!
========================================

.. image:: images/logo.jpeg
   :alt: Mangetamain Logo
   :align: center

Mangetamain is a modern Streamlit-based web application designed for data analysis and visualization. This documentation provides comprehensive information about the application's architecture, installation, usage, and API reference.

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   installation/index
   development/index
   modules

Features
--------

* **Modern Web Interface**: Built with Streamlit for an intuitive user experience
* **Data Analysis**: Comprehensive tools for data exploration and visualization
* **Docker Support**: Easy deployment with containerization
* **Testing**: Comprehensive test suite with unit and integration tests
* **Code Quality**: Automated linting, formatting, and pre-commit hooks

Quick Start
-----------

If you're eager to get started quickly:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/Hugosh71/Projet_Mangetamain.git
   cd Projet_Mangetamain

   # Install dependencies
   make requirements

   # Run the application
   make run

   # or use docker
   docker compose up app

The application will be available at `http://localhost:8501`.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
