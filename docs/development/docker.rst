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
