"""
Mechanic model module.

Represents a mechanic / technician working at the repair shop.
"""

from durus.persistent import Persistent


class Mechanic(Persistent):
    """A mechanic with a name and area of specialty."""

    def __init__(self, name="", specialty=""):
        self.name = name
        self.specialty = specialty

    def to_dict(self) -> dict:
        """Serialize the mechanic to a plain dictionary."""
        return {
            "name": self.name,
            "specialty": self.specialty,
        }
