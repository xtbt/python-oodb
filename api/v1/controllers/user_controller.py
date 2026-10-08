"""
User controller module.

Handles HTTP requests for the /users resource (CRUD operations).
Uses the base controller pattern for standard operations.
"""

from api.v1.controllers.base_controller import BaseController
from api.v1.database.repositories.user_repository import UserRepository
from api.v1.validators.user_validator import UserValidator
from api.v1.models.user import User


class UserController(BaseController):
    """REST controller for User entities."""

    repository_class = UserRepository
    validator_class = UserValidator
    model_class = User
    entity_name = "User"
    _model_fields = ["username", "password", "role"]

    def _build_model(self, data: dict):
        """
        Build a User instance from validated request data.

        :param data: validated request body
        :return: new User instance
        """
        return User(
            username=data.get("username", ""),
            password=data.get("password", ""),
            role=data.get("role", "user"),
        )
