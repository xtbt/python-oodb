"""
Part model module.

Represents a spare part or component used in service orders.
"""

from durus.persistent import Persistent


class Part(Persistent):
    """A spare part with a name and unit price."""

    def __init__(self, name="", price=0.0):
        self.name = name
        self.price = price

    def to_dict(self) -> dict:
        """Serialize the part to a plain dictionary."""
        return {
            "name": self.name,
            "price": self.price,
        }
