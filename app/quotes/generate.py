"""Module for generating HTML content for quote messages using Jinja2 templates"""

from jinja2 import Environment, FileSystemLoader

from app import config
from app.quotes.models import Messages
from app.quotes.color import get_nick_color


def generate_messages(form: Messages) -> str:
    """Generates the HTML content for rendering the quote messages

    Parameters:
        form (``Messages``): The `Messages` object containing a list of quotes, text color, 
                             and background color. This includes all the necessary information 
                             for generating the quote images, such as author details, quote text,
                             and formatting
    """
    env = Environment(
        loader=FileSystemLoader(str(config.defaults.templates_path)),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template("quote.jinja2")

    return template.render(
        messages=form.messages,
        quote_color=form.quote_color,
        text_color=form.text_color,
        get_nick_color=get_nick_color
    )
