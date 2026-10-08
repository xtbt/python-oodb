"""
Motorcycle repository module.

Handles persistence operations for Motorcycle entities.
"""

from api.v1.database.repository import BaseRepository


class MotorcycleRepository(BaseRepository):
    """Repository for Motorcycle objects, stored in the 'motorcycles' collection."""

    collection_name = "motorcycles"
