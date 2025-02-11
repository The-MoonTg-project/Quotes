"""Initializes the FastAPI application and loads the configuration"""

from fastapi import FastAPI
from app.config import parse_config

__version__ = "1.0"

config = parse_config()
api = FastAPI(title="Quotes API", version=__version__)
