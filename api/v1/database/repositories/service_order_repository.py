"""
Service order repository module.

Handles persistence operations for ServiceOrder entities.
"""

from api.v1.database.repository import BaseRepository


class ServiceOrderRepository(BaseRepository):
    """Repository for ServiceOrder objects, stored in the 'orders' collection."""

    collection_name = "orders"
