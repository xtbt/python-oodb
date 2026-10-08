"""
Car controller module.

Handles HTTP requests for the /cars resource.
"""

from api.v1.controllers.base_controller import BaseController
from api.v1.database.repositories.car_repository import CarRepository
from api.v1.validators.car_validator import CarValidator
from api.v1.models.vehicle import Car


class CarController(BaseController):
    """REST controller for Car entities."""

    repository_class = CarRepository
    validator_class = CarValidator
    model_class = Car
    entity_name = "Car"
    _model_fields = ["plate", "make", "model", "year", "door_count"]
