"""
Motorcycle request validator module.
"""

from api.v1.validators.base_validator import BaseValidator


class MotorcycleValidator(BaseValidator):
    """Validates request data for Motorcycle operations."""

    # -- Fields required when creating a motorcycle --
    REQUIRED_FIELDS = ["plate", "make", "model", "year", "engine_displacement_cc"]

    @classmethod
    def validate_create(cls, data: dict) -> list:
        """
        Validate the request body for creating a new motorcycle.

        :param data: parsed request body
        :return: list of error messages (empty if valid)
        """
        errors = cls.require_fields(data, cls.REQUIRED_FIELDS)
        errors += cls.validate_type(data, "year", int, "integer")
        errors += cls.validate_type(data, "engine_displacement_cc", int, "integer")
        return errors
