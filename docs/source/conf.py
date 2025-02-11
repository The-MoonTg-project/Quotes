# Project information
project = "Quotes"
copyright = "2024, Fl1yd"
author = "Fl1yd"
release = "1.0"

# Templates
html_theme = "furo"
html_favicon = "_static/favicon.ico"

html_static_path = ["_static"]
html_theme_options = {
    "light_logo": "logo_light.svg",
    "dark_logo": "logo_dark.svg",
}

master_doc = "toc"
index_doc = "index"

# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode"
]
