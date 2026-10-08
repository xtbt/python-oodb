"""
HTTP headers configuration module.

Provides default headers applied to every API response,
including CORS headers for cross-origin requests.
"""


class Headers:
    """Manages default HTTP response headers."""

    # -- Default headers applied to every response --
    DEFAULT = {
        "Content-Type": "application/json; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "X-Content-Type-Options": "nosniff",
    }

    @classmethod
    def get_all(cls) -> dict:
        """Return a copy of the default headers dictionary."""
        return dict(cls.DEFAULT)
