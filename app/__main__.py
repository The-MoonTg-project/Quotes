"""Main entry point for running the application"""

import uvicorn

from app import api, config
from app.logger import setup_logger

from app import routers  # pylint: disable=unused-import


if __name__ == "__main__":
    setup_logger(level=config.settings.logging.level)
    uvicorn.run(api, port=config.settings.server.port, log_config=None)
