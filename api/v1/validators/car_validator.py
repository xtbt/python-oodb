"""
Car request validator module.
"""

from api.v1.validators.base_validator import BaseValidator


class CarValidator(BaseValidator):
    """Validates request data for Car operations."""

    # -- Fields required when creating a car --
    REQUIRED_FIELDS = ["plate", "make", "model", "year", "door_count"]

    @classmethod
    def validate_create(cls, data: dict) -> list:
        """
        Validate the request body for creating a new car.

        :param data: parsed request body
        :return: list of error messages (empty if valid)
        """
        errors = cls.require_fields(data, cls.REQUIRED_FIELDS)
        errors += cls.validate_type(data, "year", int, "integer")
        errors += cls.validate_type(data, "door_count", int, "integer")
        return errors
