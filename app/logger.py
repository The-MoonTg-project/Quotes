"""Logger setup"""

import logging

from typing import List, Union, Optional
from loguru import logger


class InterceptHandler(logging.Handler):
    """Intercepts standard logging messages and redirects them to Loguru logger"""

    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame = logging.currentframe()
        depth = 2

        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logger(level: Union[str, int] = logging.INFO, ignored: Optional[List[str]] = None):
    """Sets up the logger with the specified level and disables logs for specified modules

    Parameters:
        level (``str`` | ``int``, optional):
            The logging level, default is "INFO"

        ignored (``List[str]``, optional):
            A list of loggers to be disabled
    """
    if not ignored:
        ignored = []

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.getLevelName(level))
    for ignore in ignored:
        logger.disable(ignore)
