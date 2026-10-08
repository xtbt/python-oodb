"""
Part repository module.

Handles persistence operations for Part entities.
"""

from api.v1.database.repository import BaseRepository


class PartRepository(BaseRepository):
    """Repository for Part objects, stored in the 'parts' collection."""

    collection_name = "parts"
