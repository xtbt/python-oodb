"""
Part controller module.

Handles HTTP requests for the /parts resource.
"""

from api.v1.controllers.base_controller import BaseController
from api.v1.database.repositories.part_repository import PartRepository
from api.v1.validators.part_validator import PartValidator
from api.v1.models.part import Part


class PartController(BaseController):
    """REST controller for Part entities."""

    repository_class = PartRepository
    validator_class = PartValidator
    model_class = Part
    entity_name = "Part"
    _model_fields = ["name", "price"]
