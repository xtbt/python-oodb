"""
Service order request validator module.
"""

from api.v1.validators.base_validator import BaseValidator


class ServiceOrderValidator(BaseValidator):
    """Validates request data for ServiceOrder operations."""

    # -- Fields required when creating a service order --
    REQUIRED_FIELDS = [
        "order_number",
        "vehicle_type",
        "vehicle_id",
        "mechanic_id",
        "description",
        "labor_cost",
    ]

    @classmethod
    def validate_create(cls, data: dict) -> list:
        """
        Validate the request body for creating a new service order.

        :param data: parsed request body
        :return: list of error messages (empty if valid)
        """
        errors = cls.require_fields(data, cls.REQUIRED_FIELDS)
        errors += cls.validate_type(data, "vehicle_id", int, "integer")
        errors += cls.validate_type(data, "mechanic_id", int, "integer")
        errors += cls.validate_type(data, "labor_cost", (int, float), "number")

        # -- Validate vehicle_type is either 'car' or 'motorcycle' --
        vehicle_type = data.get("vehicle_type")
        if vehicle_type and vehicle_type not in ("car", "motorcycle"):
            errors.append("Field 'vehicle_type' must be 'car' or 'motorcycle'.")

        # -- part_ids is optional but must be a list of integers if present --
        part_ids = data.get("part_ids")
        if part_ids is not None and not isinstance(part_ids, list):
            errors.append("Field 'part_ids' must be a list of integers.")

        return errors
