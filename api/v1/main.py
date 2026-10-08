"""
API entry point module.

Creates the HTTP server using only the standard library http.server,
registers all routes, and starts listening for requests.
"""

import sys
import os
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

# -- Ensure the project root is in the Python path --
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.v1.core.config import Config
from api.v1.core.router import Router
from api.v1.core.request import Request
from api.v1.core.response import Response
from api.v1.core.headers import Headers
from api.v1.database.connection import DatabaseConnection

# -- Import all controllers --
from api.v1.controllers.car_controller import CarController
from api.v1.controllers.motorcycle_controller import MotorcycleController
from api.v1.controllers.mechanic_controller import MechanicController
from api.v1.controllers.part_controller import PartController
from api.v1.controllers.service_order_controller import ServiceOrderController
from api.v1.controllers.auth_controller import AuthController
from api.v1.controllers.user_controller import UserController


def _register_crud(router: Router, prefix: str, controller):
    """
    Helper: register the five standard CRUD routes for a controller.

    :param router: the Router instance
    :param prefix: URL prefix (e.g. '/cars')
    :param controller: controller instance with list_all, get_one, create, update, delete
    """
    router.add_route("GET", prefix, controller.list_all)
    router.add_route("GET", f"{prefix}/{{id}}", controller.get_one)
    router.add_route("POST", prefix, controller.create)
    router.add_route("PUT", f"{prefix}/{{id}}", controller.update)
    router.add_route("DELETE", f"{prefix}/{{id}}", controller.delete)


def register_routes(router: Router):
    """
    Register all API routes on the given router.

    Must be called AFTER DatabaseConnection.initialize() because
    controllers instantiate repositories that need the DB connection.

    To add a new entity, instantiate its controller and
    call _register_crud() with the desired URL prefix.
    """

    # -- Cars --
    _register_crud(router, "/cars", CarController())

    # -- Motorcycles --
    _register_crud(router, "/motorcycles", MotorcycleController())

    # -- Mechanics --
    _register_crud(router, "/mechanics", MechanicController())

    # -- Parts --
    _register_crud(router, "/parts", PartController())

    # -- Service Orders --
    _register_crud(router, "/orders", ServiceOrderController())

    # -- Users (CRUD) --
    _register_crud(router, "/users", UserController())

    # -- Authentication --
    auth = AuthController()
    router.add_route("POST", "/auth/register", auth.register)
    router.add_route("POST", "/auth/login", auth.login)


# -- Module-level router instance, populated after DB init in main() --
_router = Router()


class APIRequestHandler(BaseHTTPRequestHandler):
    """
    Custom HTTP request handler.

    Routes incoming requests through the Router and dispatches
    them to the appropriate controller method.
    """

    def _handle_request(self):
        """Shared handler for all HTTP methods."""
        # -- Build high-level Request and Response objects --
        request = Request(self)
        response = Response(self)

        # -- Resolve the route --
        handler, kwargs = _router.resolve(request.method, request.path)

        if handler is None:
            # -- No matching route found --
            response.not_found(f"No route matches {request.method} {request.path}")
            return

        try:
            # -- Call the controller method --
            handler(request, response, **kwargs)
        except Exception as e:
            # -- Catch unexpected errors and return a 500 --
            print(f"[ERROR] {request.method} {request.path}: {e}")
            response.internal_error(str(e))

    def do_GET(self):
        """Handle GET requests."""
        self._handle_request()

    def do_POST(self):
        """Handle POST requests."""
        self._handle_request()

    def do_PUT(self):
        """Handle PUT requests."""
        self._handle_request()

    def do_DELETE(self):
        """Handle DELETE requests."""
        self._handle_request()

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(204)
        for key, value in Headers.get_all().items():
            self.send_header(key, value)
        self.end_headers()

    def log_message(self, format, *args):
        """Override default logging to include a cleaner format."""
        print(f"[{self.log_date_time_string()}] {args[0]}")


def main():
    """Initialize the database, start the HTTP server, and serve forever."""
    # -- Initialize the Durus database connection --
    DatabaseConnection.initialize(Config.DB_PATH)
    print(f"Database initialized at: {Config.DB_PATH}")

    # -- Register all routes (must happen after DB init) --
    register_routes(_router)

    # -- Create and start the HTTP server --
    server = ThreadingHTTPServer((Config.HOST, Config.PORT), APIRequestHandler)
    print(f"API server running on http://{Config.HOST}:{Config.PORT}{Config.API_PREFIX}")
    print("Press Ctrl+C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # -- Clean up database connection --
        DatabaseConnection.get_instance().close()
        server.server_close()
        print("Server stopped.")


if __name__ == "__main__":
    main()
