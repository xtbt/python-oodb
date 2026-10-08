"""
Car repository module.

Handles persistence operations for Car entities.
"""

from api.v1.database.repository import BaseRepository


class CarRepository(BaseRepository):
    """Repository for Car objects, stored in the 'cars' collection."""

    collection_name = "cars"
