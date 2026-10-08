"""
HTTP response builder module.

Provides a fluent interface for constructing JSON responses
with proper status codes and headers.
"""

import json
from api.v1.core.headers import Headers


class Response:
    """Builds and sends an HTTP JSON response."""

    def __init__(self, handler):
        """
        :param handler: the raw BaseHTTPRequestHandler instance
        """
        self._handler = handler

    def send(self, status_code: int, body: dict = None):
        """
        Send a JSON response to the client.

        :param status_code: HTTP status code (e.g. 200, 404)
        :param body: dictionary to serialize as JSON
        """
        # -- Serialize body to JSON bytes --
        response_body = json.dumps(body or {}, ensure_ascii=False).encode("utf-8")

        # -- Write the status line --
        self._handler.send_response(status_code)

        # -- Apply all default headers --
        for key, value in Headers.get_all().items():
            self._handler.send_header(key, value)

        # -- Set content length --
        self._handler.send_header("Content-Length", str(len(response_body)))
        self._handler.end_headers()

        # -- Write the body --
        self._handler.wfile.write(response_body)

    # -- Convenience methods for common responses --

    def ok(self, data=None, message: str = "Success"):
        """200 OK"""
        self.send(200, {"status": "success", "message": message, "data": data})

    def created(self, data=None, message: str = "Resource created"):
        """201 Created"""
        self.send(201, {"status": "success", "message": message, "data": data})

    def bad_request(self, errors=None, message: str = "Bad request"):
        """400 Bad Request"""
        self.send(400, {"status": "error", "message": message, "errors": errors})

    def unauthorized(self, message: str = "Unauthorized"):
        """401 Unauthorized"""
        self.send(401, {"status": "error", "message": message})

    def not_found(self, message: str = "Resource not found"):
        """404 Not Found"""
        self.send(404, {"status": "error", "message": message})

    def method_not_allowed(self, message: str = "Method not allowed"):
        """405 Method Not Allowed"""
        self.send(405, {"status": "error", "message": message})

    def internal_error(self, message: str = "Internal server error"):
        """500 Internal Server Error"""
        self.send(500, {"status": "error", "message": message})
