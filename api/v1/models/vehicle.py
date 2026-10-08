"""
Vehicle models module.

Defines the Vehicle base class and its subclasses Car and Motorcycle.
All inherit from durus.persistent.Persistent so they can be stored
in the object-oriented database.
"""

from durus.persistent import Persistent


class Vehicle(Persistent):
    """
    Base class for all vehicles.

    Contains the common fields shared by every vehicle type.
    Subclasses add their own specific fields.
    """

    def __init__(self, plate="", make="", model="", year=0):
        self.plate = plate
        self.make = make
        self.model = model
        self.year = year

    def description(self) -> str:
        """Return a human-readable summary of the vehicle."""
        return f"{self.make} {self.model} ({self.year}) - plate {self.plate}"

    def kind(self) -> str:
        """Return the class name (e.g. 'Car', 'Motorcycle')."""
        return self.__class__.__name__

    def to_dict(self) -> dict:
        """Serialize the vehicle to a plain dictionary."""
        return {
            "plate": self.plate,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "kind": self.kind(),
        }


class Car(Vehicle):
    """A car with a specific door count."""

    def __init__(self, plate="", make="", model="", year=0, door_count=0):
        super().__init__(plate, make, model, year)
        self.door_count = door_count

    def description(self) -> str:
        """Return a human-readable summary including door count."""
        return f"[Car] {super().description()} - {self.door_count} doors"

    def to_dict(self) -> dict:
        """Serialize the car to a plain dictionary."""
        data = super().to_dict()
        data["door_count"] = self.door_count
        return data


class Motorcycle(Vehicle):
    """A motorcycle with engine displacement in cubic centimeters."""

    def __init__(self, plate="", make="", model="", year=0, engine_displacement_cc=0):
        super().__init__(plate, make, model, year)
        self.engine_displacement_cc = engine_displacement_cc

    def description(self) -> str:
        """Return a human-readable summary including engine displacement."""
        return f"[Motorcycle] {super().description()} - {self.engine_displacement_cc}cc"

    def to_dict(self) -> dict:
        """Serialize the motorcycle to a plain dictionary."""
        data = super().to_dict()
        data["engine_displacement_cc"] = self.engine_displacement_cc
        return data
