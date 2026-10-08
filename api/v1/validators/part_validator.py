"""
Part request validator module.
"""

from api.v1.validators.base_validator import BaseValidator


class PartValidator(BaseValidator):
    """Validates request data for Part operations."""

    # -- Fields required when creating a part --
    REQUIRED_FIELDS = ["name", "price"]

    @classmethod
    def validate_create(cls, data: dict) -> list:
        """
        Validate the request body for creating a new part.

        :param data: parsed request body
        :return: list of error messages (empty if valid)
        """
        errors = cls.require_fields(data, cls.REQUIRED_FIELDS)
        errors += cls.validate_type(data, "price", (int, float), "number")
        return errors
