"""
URL router module.

Maps URL patterns to controller methods. Supports dynamic
path segments (e.g. /cars/{id}) using simple pattern matching.
"""

import re
from api.v1.core.config import Config


class Router:
    """
    Registers URL routes and dispatches incoming requests
    to the appropriate controller method.
    """

    def __init__(self):
        # -- List of registered routes: (method, compiled_regex, handler_func) --
        self._routes = []

    def add_route(self, method: str, path: str, handler):
        """
        Register a route.

        :param method: HTTP method (GET, POST, PUT, DELETE)
        :param path: URL pattern relative to API_PREFIX, e.g. "/cars" or "/cars/{id}"
        :param handler: callable(request, response, **kwargs)
        """
        # -- Build the full path with API prefix --
        full_path = Config.API_PREFIX + path

        # -- Convert {param} placeholders to named regex groups --
        pattern = re.sub(r"\{(\w+)\}", r"(?P<\1>[^/]+)", full_path)

        # -- Compile to a regex that matches the full URL --
        compiled = re.compile(f"^{pattern}$")

        self._routes.append((method.upper(), compiled, handler))

    def resolve(self, method: str, path: str):
        """
        Find the handler matching the given method and path.

        :param method: HTTP method
        :param path: request URL path
        :return: (handler, kwargs) tuple or (None, None) if no match
        """
        for route_method, pattern, handler in self._routes:
            # -- Check method and path pattern --
            if route_method == method.upper():
                match = pattern.match(path)
                if match:
                    return handler, match.groupdict()

        return None, None
