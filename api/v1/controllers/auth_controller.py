"""
Authentication controller module.

Handles user registration and simple username/password login.
No tokens or advanced auth mechanisms — just credential verification.
"""

from api.v1.database.repositories.user_repository import UserRepository
from api.v1.validators.user_validator import UserValidator
from api.v1.models.user import User


class AuthController:
    """Handles /auth/register and /auth/login endpoints."""

    def __init__(self):
        """Instantiate the user repository."""
        self.repository = UserRepository()

    def register(self, request, response, **kwargs):
        """
        POST /auth/register — create a new user account.

        Checks for duplicate usernames before persisting.
        """
        data = request.json()

        # -- Validate request body --
        errors = UserValidator.validate_create(data)
        if errors:
            response.bad_request(errors=errors)
            return

        # -- Check if the username already exists --
        existing_id, _ = self.repository.find_by_username(data["username"])
        if existing_id is not None:
            response.bad_request(errors=["Username already exists."])
            return

        # -- Create the user --
        user = User(
            username=data["username"],
            password=data["password"],
            role=data.get("role", "user"),
        )
        user_id = self.repository.create(user)
        response.created(data={"id": user_id, **user.to_dict()})

    def login(self, request, response, **kwargs):
        """
        POST /auth/login — authenticate with username and password.

        Returns user data on success, or 401 on failure.
        """
        data = request.json()

        # -- Validate request body --
        errors = UserValidator.validate_login(data)
        if errors:
            response.bad_request(errors=errors)
            return

        # -- Look up the user --
        user_id, user = self.repository.find_by_username(data["username"])
        if user is None:
            response.unauthorized("Invalid username or password.")
            return

        # -- Verify the password --
        if not user.check_password(data["password"]):
            response.unauthorized("Invalid username or password.")
            return

        response.ok(data={"id": user_id, **user.to_dict()}, message="Login successful.")
