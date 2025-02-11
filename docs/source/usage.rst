Usage
=====

This guide will walk you through how to use the **Quotes API** to generate customizable quote images


Starting the API
----------------

To start using the **Quotes API**, ensure that you have followed the :doc:`Installation Guide <installation.rst>` and have the FastAPI server running. Once the server is up and running, you can interact with the API using the following endpoint:

- **Endpoint**: ``/generate``
- **Method**: ``POST``
- **Description**: Generates a quote image based on the provided input


Example POST Request
--------------------

Here is an example of a POST request to generate a quote image:

.. code-block:: bash

    curl -X POST "http://127.0.0.1:1337/generate" \
    -H "Content-Type: application/json" \
    -d '{
        "messages": [
            {
                "text": "This is a sample quote",
                "author": {
                    "id": 1,
                    "name": "John Doe"
                }
            }
        ]
    }'


Request Structure
-----------------

In the body of the POST request, you need to provide a JSON object with the following fields:

.. code-block:: json

    {
        "messages": [
            {
            "text": "This is a quote",
            "author": {
                "id": 1,
                "name": "Author Name",
                "avatar": "optional base64 image",
                "rank": "optional rank",
                "via_bot": "optional bot name"
            },
            "reply": {
                "id": 2,
                "name": "Optional Reply Name",
                "text": "Optional reply text"
            },
            "media": "optional base64 image"
            }
        ],
        "quote_color": "#000000",
        "text_color": "white"
    }


Field Definitions
-----------------

The following table describes the fields that you can include in the POST request based on the models:

.. list-table:: POST request fields
    :header-rows: 1

    * - Field
      - Type
      - Description
    * - `messages`
      - List of Quote
      - **Required**. A list of ``Quote`` objects, representing each quote in the image
    * - `text_color`
      - String
      - **Optional**. Text color for the quote. If not provided, the default value from the configuration will be used
    * - `quote_color`
      - String
      - **Optional**. Background color for the quote. If not provided, the default value from the configuration will be used


Quote fields
------------

The ``Quote`` object contains the following fields:

.. list-table:: Quote fields
    :header-rows: 1

    * - Field
      - Type
      - Description
    * - `text`
      - String
      - **Optional**. The main quote text for the message. If not provided, the message will only display the media or reply if they exist
    * - `media`
      - String (Base64)
      - **Optional**. Base64-encoded image attached to the quote (e.g., for sharing images or pictures in the quote)
    * - `entities`
      - List of Entity
      - **Optional**. List of formatting entities applied to the text, such as bold, italic, underline, and others
    * - `author`
      - Author
      - **Required**. Object representing the ``Author`` of the quote
    * - `reply`
      - Reply
      - **Optional**. Object representing the reply to the message


Author fields
-------------

The ``Author`` object contains the following fields:

.. list-table:: Author fields
    :header-rows: 1

    * - Field
      - Type
      - Description
    * - `id`
      - Integer
      - **Required**. Unique identifier for the author
    * - `name`
      - String
      - **Required**. The name of the author
    * - `avatar`
      - String (Base64)
      - **Optional**. Base64-encoded image for the author's avatar
    * - `rank`
      - String
      - **Optional**. The rank or title of the author (e.g., "Admin", "Moderator")
    * - `via_bot`
      - String
      - **Optional**. Bot name if the message was sent via a bot


Reply fields
------------

The ``Reply`` object contains the following fields:

.. list-table:: Reply fields
    :header-rows: 1

    * - Field
      - Type
      - Description
    * - `id`
      - Integer
      - **Optional**. Unique identifier for the reply author
    * - `name`
      - String
      - **Optional**. Name of the reply author
    * - `text`
      - String
      - **Optional**. The reply text


Entity fields
-------------

The ``Entity`` object represents formatting applied to portions of the text (bold, italic, underline, etc.) and contains the following fields:

.. list-table:: Entity fields
    :header-rows: 1

    * - `offset`
      - Integer
      - **Required**. The position in the text where the formatting starts
    * - `length`
      - Integer
      - **Required**. The number of characters that the formatting applies to
    * - `type`
      - String (Literal)
      - **Required**. The type of formatting applied to the text
