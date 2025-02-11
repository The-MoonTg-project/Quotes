"""Utility functions for handling emoji in quote messages"""

import regex


def replace_emoji(text: str) -> str:
    """Replaces emoji characters in a text with HTML span elements for rendering

    Parameters:
        text (``str``): The input text that may contain emoji characters. This text will be 
                        processed, and all emoji found will be replaced with corresponding HTML 
                        elements
    """
    pattern = regex.compile(r"[\p{Emoji_Presentation}\p{Extended_Pictographic}]", regex.UNICODE)
    return pattern.sub(
        lambda match: f"<span style=\"font-family: 'Noto Color Emoji';\">{match.group(0)}</span>",
        text
    )
