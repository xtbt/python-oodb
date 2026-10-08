"""
Service order model module.

Represents a repair/service order that links a vehicle,
a mechanic, and a list of parts together.
"""

from durus.persistent import Persistent
from durus.persistent_list import PersistentList


class ServiceOrder(Persistent):
    """
    A service order that holds direct references to other
    persistent objects (vehicle, mechanic, parts).

    Durus automatically persists all reachable Persistent objects,
    so references are stored as real object pointers, not IDs.
    """

    def __init__(
        self,
        order_number="",
        vehicle=None,
        mechanic=None,
        parts=None,
        description="",
        status="open",
        labor_cost=0.0,
    ):
        self.order_number = order_number
        # -- Direct reference to the Vehicle object (Car or Motorcycle) --
        self.vehicle = vehicle
        # -- Direct reference to the Mechanic object --
        self.mechanic = mechanic
        # -- PersistentList of Part objects (not IDs) --
        self.parts = PersistentList(parts or [])
        self.description = description
        self.status = status
        self.labor_cost = labor_cost

    def total_cost(self) -> float:
        """Calculate total cost: labor + sum of part prices."""
        parts_cost = sum(p.price for p in self.parts)
        return self.labor_cost + parts_cost

    def to_dict(self) -> dict:
        """Serialize the service order to a plain dictionary."""
        return {
            "order_number": self.order_number,
            "vehicle": self.vehicle.to_dict() if self.vehicle else None,
            "mechanic": self.mechanic.to_dict() if self.mechanic else None,
            "parts": [p.to_dict() for p in self.parts],
            "description": self.description,
            "status": self.status,
            "labor_cost": self.labor_cost,
            "total_cost": self.total_cost(),
        }
