"""
Mechanic controller module.

Handles HTTP requests for the /mechanics resource.
"""

from api.v1.controllers.base_controller import BaseController
from api.v1.database.repositories.mechanic_repository import MechanicRepository
from api.v1.validators.mechanic_validator import MechanicValidator
from api.v1.models.mechanic import Mechanic


class MechanicController(BaseController):
    """REST controller for Mechanic entities."""

    repository_class = MechanicRepository
    validator_class = MechanicValidator
    model_class = Mechanic
    entity_name = "Mechanic"
    _model_fields = ["name", "specialty"]
