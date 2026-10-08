"""
Mechanic request validator module.
"""

from api.v1.validators.base_validator import BaseValidator


class MechanicValidator(BaseValidator):
    """Validates request data for Mechanic operations."""

    # -- Fields required when creating a mechanic --
    REQUIRED_FIELDS = ["name", "specialty"]

    @classmethod
    def validate_create(cls, data: dict) -> list:
        """
        Validate the request body for creating a new mechanic.

        :param data: parsed request body
        :return: list of error messages (empty if valid)
        """
        errors = cls.require_fields(data, cls.REQUIRED_FIELDS)
        return errors
