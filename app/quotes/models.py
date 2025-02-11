"""Data models"""

import html

from typing import List, Tuple, Optional
from pydantic import BaseModel, model_validator

from app import config
from app.quotes.emoji import replace_emoji
from app.quotes.text_utils import add_surrogate, del_surrogate, within_surrogate


class Entity(BaseModel):
    """This class represents a text formatting entity (like bold, italic, underline, etc.) 
    applied to portions of the text in a quote. Each entity specifies the range of characters 
    it affects and the type of formatting

    Attributes:
        offset (``int``): The starting position in the text where the formatting begins

        length (``int``): The number of characters affected by the entity

        type (``str``): The type of entity
    """

    offset: int
    length: int
    type: str


class Reply(BaseModel):
    """This class represents a reply to a quote message. Replies are optional, and they 
    contain details about the user who made the reply and the reply text

    Attributes:
        id (``int``, optional): The unique identifier of the reply author

        name (``str``, optional): The name of the reply author

        text (``str``, optional): The text of the reply
    """

    id: Optional[int] = None
    name: Optional[str] = None
    text: Optional[str] = None

    @model_validator(mode="after")
    def _prepare_reply(cls, model: "Reply") -> "Reply":
        if model.name:
            model.name = replace_emoji(html.escape(model.name))
        if model.text:
            model.text = replace_emoji(html.escape(model.text))

        return model


class Author(BaseModel):
    """This class represents the author of a quote. It contains details about the author, 
    such as their name, avatar, and optionally a rank or bot information if the message was 
    sent via a bot

    Attributes:
        id (``int``): The unique identifier of the author

        name (``str``): The name of the author

        avatar (``str``, optional): Base64-encoded image for the author's avatar

        rank (``str``, optional): The rank or title of the author (e.g., "CEO", "Manager")

        via_bot (``str``, optional): The bot name if the message was sent via a bot
    """

    id: int
    name: str
    avatar: Optional[str] = None
    rank: Optional[str] = None
    via_bot: Optional[str] = None

    @model_validator(mode="after")
    def _prepare_author(cls, model: "Author") -> "Author":
        model.name = replace_emoji(html.escape(model.name))
        return model


class Quote(BaseModel):
    """This class represents a single quote message. A quote consists of the main text, 
    optional media (such as an image), and the author. It can also include optional entities 
    for formatting text and an optional reply to the message

    Attributes:
        text (``str``, optional): The main text of the quote. If not provided, 
                                  the message will focus on other elements such as 
                                  media or reply

        media (``str``, optional): Base64-encoded image attached to the quote 
                                   (e.g., an image related to the message)

        entities (``List[Entity]``, optional): A list of formatting entities 
                                               applied to the text, such as bold, 
                                               italic, underline, etc.

        author (``Author``): The author of the quote, containing details like their name, ID, 
                             and avatar

        reply (``Reply``, optional): An optional reply to the message, representing 
                                     another message that replies to this one
    """

    text: Optional[str] = None
    media: Optional[str] = None
    entities: Optional[List[Entity]] = None
    author: Author
    reply: Optional[Reply] = None

    @model_validator(mode="after")
    def _prepare_quote(cls, model: "Quote") -> "Quote":
        if model.text:
            if not model.entities:
                model.text = html.escape(model.text)
                model.text = model.text.replace(" ", "&nbsp;<wbr>").replace("\n", "<br>")
            else:
                model.text = add_surrogate(model.text)

                format_inserts: List[Tuple[int, int, str]] = []
                for index, entity in enumerate(model.entities):
                    start = entity.offset
                    end = entity.offset + entity.length
                    delimiter = config.defaults.entity_map.get(entity.type, ("<a>", "</a>"))

                    format_inserts.append((start, index, delimiter[0]))
                    format_inserts.append((end, -index, delimiter[1]))

                format_inserts.sort(key=lambda point: (point[0], point[1]))
                escape_bound = len(model.text)

                while format_inserts:
                    position, _, text = format_inserts.pop()
                    while within_surrogate(model.text, position):
                        position += 1

                    model.text = (
                        model.text[:position]
                        + text
                        + html.escape(model.text[position:escape_bound])
                        + model.text[escape_bound:]
                    )
                    escape_bound = position

                model.text = html.escape(model.text[:escape_bound]) + model.text[escape_bound:]
                model.text = model.text.replace(" ", "&nbsp;<wbr>").replace("\n", "<br>")
                model.text = del_surrogate(model.text)

            model.text = replace_emoji(model.text)

        if model.reply and not any([model.reply.id, model.reply.name, model.reply.text]):
            model.reply = None

        return model


class Messages(BaseModel):
    """This class represents a collection of messages, each containing one or more quotes. 
    It is used to send multiple quotes as a batch request to generate quote images. 
    In addition to the quotes themselves, it also includes optional settings 
    for text color and quote background color

    Attributes:
        messages (``List[Quote]``): A list of `Quote` objects that represent the individual 
                                    messages in a batch request

        text_color (``str``, optional): The color of the text, specified as a valid 
                                        CSS color string (e.g., "black", "#000000")

        quote_color (``str``, optional): The background color of the quote, specified 
                                         as a valid CSS color string (e.g., "#ffffff")
    """

    messages: List[Quote]
    text_color: Optional[str] = config.settings.quote.text_color
    quote_color: Optional[str] = config.settings.quote.background_color
