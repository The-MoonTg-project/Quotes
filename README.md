<p align="center">
    <b>Quotes API</b>: Quote Image Generator
</p>


<h1>What is this?</h1>

Quotes API is a FastAPI-based service that allows users to generate visually appealing quote images resembling Telegram messages


<h1>Installing</h1>

> Before installing Quotes API, ensure you have <code>Poetry</code> installed. You can install Poetry by following the [Poetry installation guide](https://python-poetry.org/docs/#installation)

Once Poetry is installed, clone the repository and install dependencies:

<pre lang="bash">
git clone https://github.com/Fl1yd/Quotes
cd Quotes
poetry install
</pre>

Additionally, ensure <code>wkhtmltopdf</code> version 0.12.5 is installed on your system:

Download the appropriate package for your distribution from the wkhtmltopdf releases page

Install it using your package manager. For example, on Ubuntu:

<pre lang="bash">
sudo apt-get install -y wkhtmltopdf=0.12.5
</pre>

> Note: If the specific version is not available in your package manager, you may need to download the binary directly and follow the installation instructions provided in the release notes


<h1>Usage</h1>

To use Quotes API, start the FastAPI application:

<pre lang="bash">
poetry run python3 -m app
</pre>

The application will start on the port specified in the <code>config.toml</code> file (default is 1337). You can then access the API documentation at `http://localhost:1337/docs`


<h1>API Endpoints</h1>

Quotes API provides the following endpoint for generating quote images:

- **Generate quote image:**
    Use the <code>POST /generate</code> endpoint to generate a quote image. You need to provide a `Messages` object with the required data

<pre lang="json">
{
    "messages": [
        {
            "text": "This is a quote",
            "author": {
                "id": 1,
                "name": "Author Name"
            }
        }
    ],
    "quote_color": "#000000",
    "text_color": "white"
}
</pre>


<h1>Configuration</h1>

Customize your application settings by updating the <code>config.toml</code> file:

<pre lang="toml">
[settings]
    [settings.quote]
    quality = 85
    text_color = "white"
    background_color = "#162330"

    [settings.logging]
    level = "INFO"

    [settings.server]
    port = 1337
</pre>


<h1>License</h1>
Quotes API is licensed under the MIT License
