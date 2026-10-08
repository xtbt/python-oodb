"""
Mechanic repository module.

Handles persistence operations for Mechanic entities.
"""

from api.v1.database.repository import BaseRepository


class MechanicRepository(BaseRepository):
    """Repository for Mechanic objects, stored in the 'mechanics' collection."""

    collection_name = "mechanics"
