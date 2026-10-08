"""
Motorcycle controller module.

Handles HTTP requests for the /motorcycles resource.
"""

from api.v1.controllers.base_controller import BaseController
from api.v1.database.repositories.motorcycle_repository import MotorcycleRepository
from api.v1.validators.motorcycle_validator import MotorcycleValidator
from api.v1.models.vehicle import Motorcycle


class MotorcycleController(BaseController):
    """REST controller for Motorcycle entities."""

    repository_class = MotorcycleRepository
    validator_class = MotorcycleValidator
    model_class = Motorcycle
    entity_name = "Motorcycle"
    _model_fields = ["plate", "make", "model", "year", "engine_displacement_cc"]
