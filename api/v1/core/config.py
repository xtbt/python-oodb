"""
API configuration module.

Centralizes all configurable settings for the server,
database path, and general application parameters.
"""

import os


class Config:
    """Holds all application-wide configuration values."""

    # -- Server settings --
    HOST = os.getenv("API_HOST", "localhost")
    PORT = int(os.getenv("API_PORT", 8000))

    # -- Database settings --
    # Path to the Durus file storage (relative to project root)
    DB_PATH = os.getenv("DB_PATH", "data/api.durus")

    # -- API settings --
    API_PREFIX = "/api/v1"
