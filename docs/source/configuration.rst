Configuration
=============

This section provides an overview of the configuration options available for the **Quotes API**. The configuration is managed via the ``config.toml`` file, located in the root of the project. This file allows you to adjust various settings, such as server port, logging levels, and default quote appearance


Configuration File
------------------

The ``config.toml`` file contains several configuration sections that control different aspects of the Quotes API. Below is an example of the file:

.. literalinclude:: ../../config.toml


Sections and Settings
---------------------

``[settings.quote]``
This section defines the default appearance of the generated quote images

- **width** (``int``):
    The width of the generated quote image in pixels. *Default*: ``1792``

- **text_color** (``str``):
    The default color of the quote text. Accepts any valid CSS color value (e.g., ``"black"``, ``"#ffffff"``). *Default*: ``"white"``

- **background_color** (``str``):
    The default background color for the quote. Accepts any valid CSS color value. *Default*: ``"#162330"``


``[settings.logging]``
This section controls the logging level for the application. Logging helps with debugging and monitoring the application by outputting messages about its operations

- **level** (``str``):
    Defines the logging verbosity. Valid values are ``"DEBUG"``, ``"INFO"``, ``"WARNING"``, ``"ERROR"``, and ``"CRITICAL"``. *Default*: ``"INFO"``


``[settings.server]``
This section controls the server's behavior, such as the port on which the API will run

- **port** (``int``):
    The port on which the FastAPI application will listen for incoming requests. *Default*: ``1337``


Customizing the Configuration
-----------------------------

You can customize the behavior of the Quotes API by modifying the ``config.toml`` file. For example, to change the port number to ``8080`` and set the logging level to ``DEBUG``, you would update the file as follows:

.. code-block:: toml

    [settings]
        [settings.server]
        port = 8080

        [settings.logging]
        level = "DEBUG"
