"""
Service order controller module.

Handles HTTP requests for the /orders resource.
Overrides the default create/update logic because ServiceOrder
requires resolving object references (vehicle, mechanic, parts).
"""

from api.v1.controllers.base_controller import BaseController
from api.v1.database.repositories.service_order_repository import ServiceOrderRepository
from api.v1.database.repositories.car_repository import CarRepository
from api.v1.database.repositories.motorcycle_repository import MotorcycleRepository
from api.v1.database.repositories.mechanic_repository import MechanicRepository
from api.v1.database.repositories.part_repository import PartRepository
from api.v1.validators.service_order_validator import ServiceOrderValidator
from api.v1.models.service_order import ServiceOrder


class ServiceOrderController(BaseController):
    """REST controller for ServiceOrder entities."""

    repository_class = ServiceOrderRepository
    validator_class = ServiceOrderValidator
    model_class = ServiceOrder
    entity_name = "ServiceOrder"

    def create(self, request, response, **kwargs):
        """
        POST handler: create a service order by resolving references
        to vehicle, mechanic, and parts from their respective IDs.
        """
        data = request.json()

        # -- Validate the request body --
        errors = self.validator_class.validate_create(data)
        if errors:
            response.bad_request(errors=errors)
            return

        # -- Resolve the vehicle reference by type and ID --
        vehicle_type = data["vehicle_type"]
        vehicle_id = int(data["vehicle_id"])

        if vehicle_type == "car":
            vehicle = CarRepository().get_by_id(vehicle_id)
        else:
            vehicle = MotorcycleRepository().get_by_id(vehicle_id)

        if vehicle is None:
            response.not_found(f"Vehicle ({vehicle_type}) with id {vehicle_id} not found.")
            return

        # -- Resolve the mechanic reference --
        mechanic_id = int(data["mechanic_id"])
        mechanic = MechanicRepository().get_by_id(mechanic_id)
        if mechanic is None:
            response.not_found(f"Mechanic with id {mechanic_id} not found.")
            return

        # -- Resolve part references (optional list of IDs) --
        parts = []
        part_repo = PartRepository()
        for pid in data.get("part_ids", []):
            part = part_repo.get_by_id(int(pid))
            if part is None:
                response.not_found(f"Part with id {pid} not found.")
                return
            parts.append(part)

        # -- Build and persist the service order with real object references --
        order = ServiceOrder(
            order_number=data["order_number"],
            vehicle=vehicle,
            mechanic=mechanic,
            parts=parts,
            description=data["description"],
            status=data.get("status", "open"),
            labor_cost=float(data["labor_cost"]),
        )

        order_id = self.repository.create(order)
        response.created(data={"id": order_id, **order.to_dict()})

    def update(self, request, response, **kwargs):
        """
        PUT handler: update a service order by re-resolving references.
        """
        item_id = int(kwargs.get("id"))
        existing = self.repository.get_by_id(item_id)
        if existing is None:
            response.not_found(f"ServiceOrder with id {item_id} not found.")
            return

        data = request.json()

        # -- Validate --
        errors = self.validator_class.validate_create(data)
        if errors:
            response.bad_request(errors=errors)
            return

        # -- Resolve vehicle --
        vehicle_type = data["vehicle_type"]
        vehicle_id = int(data["vehicle_id"])
        if vehicle_type == "car":
            vehicle = CarRepository().get_by_id(vehicle_id)
        else:
            vehicle = MotorcycleRepository().get_by_id(vehicle_id)
        if vehicle is None:
            response.not_found(f"Vehicle ({vehicle_type}) with id {vehicle_id} not found.")
            return

        # -- Resolve mechanic --
        mechanic_id = int(data["mechanic_id"])
        mechanic = MechanicRepository().get_by_id(mechanic_id)
        if mechanic is None:
            response.not_found(f"Mechanic with id {mechanic_id} not found.")
            return

        # -- Resolve parts --
        parts = []
        part_repo = PartRepository()
        for pid in data.get("part_ids", []):
            part = part_repo.get_by_id(int(pid))
            if part is None:
                response.not_found(f"Part with id {pid} not found.")
                return
            parts.append(part)

        # -- Build updated order --
        order = ServiceOrder(
            order_number=data["order_number"],
            vehicle=vehicle,
            mechanic=mechanic,
            parts=parts,
            description=data["description"],
            status=data.get("status", "open"),
            labor_cost=float(data["labor_cost"]),
        )

        self.repository.update(item_id, order)
        response.ok(data={"id": item_id, **order.to_dict()}, message="ServiceOrder updated.")
