"""
HTTP request parser module.

Wraps the raw BaseHTTPRequestHandler to provide a clean
object-oriented interface for accessing method, path,
query parameters, and JSON body.
"""

import json
from urllib.parse import urlparse, parse_qs


class Request:
    """Parses and exposes HTTP request data."""

    def __init__(self, handler):
        """
        Build a Request from a BaseHTTPRequestHandler instance.

        :param handler: the raw HTTP request handler
        """
        # -- HTTP method (GET, POST, PUT, DELETE, etc.) --
        self.method = handler.command

        # -- Parse the URL into path and query string --
        parsed = urlparse(handler.path)
        self.path = parsed.path
        self.query_params = parse_qs(parsed.query)

        # -- Read request headers --
        self.headers = dict(handler.headers)

        # -- Read the raw body bytes --
        content_length = int(handler.headers.get("Content-Length", 0))
        self.raw_body = handler.rfile.read(content_length) if content_length > 0 else b""

    def json(self) -> dict:
        """
        Parse the request body as JSON.

        :return: parsed dictionary, or empty dict if body is empty/invalid
        """
        if not self.raw_body:
            return {}
        try:
            return json.loads(self.raw_body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}

    def get_param(self, name: str, default=None):
        """
        Get a single query parameter value.

        :param name: query parameter name
        :param default: fallback value if parameter is missing
        :return: first value of the parameter or the default
        """
        values = self.query_params.get(name)
        if values:
            return values[0]
        return default
