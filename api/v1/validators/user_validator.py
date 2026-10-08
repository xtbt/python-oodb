"""
User request validator module.
"""

from api.v1.validators.base_validator import BaseValidator


class UserValidator(BaseValidator):
    """Validates request data for User operations."""

    # -- Fields required when creating a user --
    REQUIRED_FIELDS = ["username", "password"]

    @classmethod
    def validate_create(cls, data: dict) -> list:
        """
        Validate the request body for creating a new user.

        :param data: parsed request body
        :return: list of error messages (empty if valid)
        """
        errors = cls.require_fields(data, cls.REQUIRED_FIELDS)

        # -- Username minimum length --
        username = data.get("username", "")
        if isinstance(username, str) and 0 < len(username) < 3:
            errors.append("Field 'username' must be at least 3 characters long.")

        # -- Password minimum length --
        password = data.get("password", "")
        if isinstance(password, str) and 0 < len(password) < 6:
            errors.append("Field 'password' must be at least 6 characters long.")

        return errors

    @classmethod
    def validate_login(cls, data: dict) -> list:
        """
        Validate the request body for login.

        :param data: parsed request body
        :return: list of error messages (empty if valid)
        """
        return cls.require_fields(data, ["username", "password"])
