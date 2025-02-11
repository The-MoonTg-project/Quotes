"""Utility functions for handling surrogate pairs in Unicode text"""

import struct


def add_surrogate(text: str):
    """Converts characters in the Supplementary Planes (above U+FFFF) to surrogate pairs in UTF-16

    Parameters:
        text (``str``): The input text that may contain characters outside the Basic Multilingual 
                        Plane (BMP). This function processes each character and, if it falls within 
                        the range U+10000 to U+10FFFF, converts it to a surrogate pair for UTF-16 
                        representation
    """
    return "".join(
        "".join(chr(low) for low in struct.unpack("<HH", char.encode("utf-16le")))
        if (0x10000 <= ord(char) <= 0x10FFFF) else char for char in text
    )


def del_surrogate(text: str):
    """Removes surrogate pairs from a string, converting them back to the Unicode character

    Parameters:
        text (``str``): A string containing surrogate pairs that need to be converted back to 
                        standard Unicode characters
    """
    return text.encode("utf-16", "surrogatepass").decode("utf-16")


def within_surrogate(text: str, index: int, *, length: int = None):
    """Checks if a specified index in a string is within a surrogate pair

    Parameters:
        text (``str``): The input string in which to check for surrogate pairs
        
        index (``int``): The position in the string to check. Determines if this index is part of 
                         a surrogate pair
        
        length (``int``, optional): An optional length parameter to restrict the range within the 
                                    string to check. If not provided, the entire length of the 
                                    text is used
    """
    if length is None:
        length = len(text)

    return (
        1 < index < len(text) and
        "\ud800" <= text[index - 1] <= "\udbff" and
        "\ud800" <= text[index] <= "\udfff"
    )
