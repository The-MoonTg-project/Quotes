"""Utility functions for handling color assignments in quote messages"""

from typing import Tuple, Union
from app import config


def get_nick_color(user_id: int) -> Union[str, Tuple[str]]:
    """Returns a color based on the user ID

    Parameters:
        user_id (``int``): The unique identifier of the user
    """
    nums = [0, 7, 4, 1, 6, 3, 5]
    return config.defaults.colors[nums[user_id % 7]]
