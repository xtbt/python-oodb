"""
Base validator module.

Provides shared validation logic that entity-specific
validators can reuse.
"""


class BaseValidator:
    """Base class for all request body validators."""

    @staticmethod
    def require_fields(data: dict, fields: list) -> list:
        """
        Check that all required fields are present and non-empty.

        :param data: the parsed request body
        :param fields: list of required field names
        :return: list of error messages (empty if valid)
        """
        errors = []
        for field in fields:
            if field not in data or data[field] is None or data[field] == "":
                errors.append(f"Field '{field}' is required.")
        return errors

    @staticmethod
    def validate_type(data: dict, field: str, expected_type, type_name: str) -> list:
        """
        Check that a field has the expected type.

        :param data: the parsed request body
        :param field: field name to check
        :param expected_type: Python type (e.g. int, str)
        :param type_name: human-readable type name for error messages
        :return: list of error messages (empty if valid)
        """
        if field in data and data[field] is not None:
            if not isinstance(data[field], expected_type):
                return [f"Field '{field}' must be of type {type_name}."]
        return []
