Installation
============

This section provides detailed steps on how to install and set up the Quotes API project

Prerequisites
-------------

Before proceeding with the installation, ensure the following dependencies are installed on your system:

1. **Python 3.9+**: Quotes API requires Python version 3.9 or higher
   
You can check your current version of Python by running:

.. code-block:: bash

    $ python3 --version

If it's not installed or the version is too low, you can download Python from the official website: `Python Downloads <https://www.python.org/downloads/>`_

2. **Poetry**: This project uses Poetry for dependency management. Poetry simplifies installing and managing dependencies

To install Poetry, follow the instructions in the official guide: `Poetry Installation <https://python-poetry.org/docs/#installation>`_

3. **wkhtmltoimage**: The project relies on ``wkhtmltoimage`` to generate quote images from HTML templates. Ensure it's installed on your system:

Download the appropriate package for your distribution and install it using your package manager. Instructions for major distributions are available on the `wkhtmltopdf downloads page <https://wkhtmltopdf.org/downloads.html>`_


Installation Steps
------------------

Once the prerequisites are installed, follow these steps to install and set up Quotes API:

1. **Clone the repository**:

First, clone the Quotes API repository from GitHub to your local machine:

.. code-block:: bash

    $ git clone https://github.com/Fl1yd/Quotes

Navigate to the project folder:

.. code-block:: bash

    $ cd Quotes

2. **Install dependencies using Poetry**:

With Poetry installed, run the following command in the project directory to install all the necessary dependencies:

.. code-block:: bash

    $ poetry install


Running the Application
-----------------------

Now that everything is installed, you can start the Quotes API server:

1. **Start the FastAPI application**:

Run the following command to launch the FastAPI application:

.. code-block:: bash

    $ poetry run python -m app

This will start the application on the port specified in the ``config.toml`` file (by default, it uses port ``1337``)

2. **Access the API documentation**:

FastAPI automatically generates API documentation, which you can access in your browser: http://127.0.0.1:1337/docs. These interactive documentation pages will help you test and explore the available endpoints
