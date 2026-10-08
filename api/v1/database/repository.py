"""
Base repository module.

Provides a generic CRUD layer on top of a Durus PersistentDict
collection. Entity-specific repositories inherit from this class
and only need to specify the collection name.
"""

from api.v1.database.connection import DatabaseConnection


class BaseRepository:
    """
    Generic repository that handles create, read, update, and delete
    operations against a named PersistentDict collection.
    """

    # -- Subclasses must set this to match a key in DatabaseConnection.COLLECTIONS --
    collection_name: str = None

    def __init__(self):
        """Get a reference to the database connection and the target collection."""
        self.db = DatabaseConnection.get_instance()
        self.collection = self.db.get_collection(self.collection_name)

    def _next_id(self) -> int:
        """
        Calculate the next auto-incremented ID for this collection.

        :return: integer ID one greater than the current maximum
        """
        if len(self.collection) == 0:
            return 1
        return max(self.collection.keys()) + 1

    def get_all(self) -> list:
        """
        Retrieve all items in the collection as a list of (id, object) tuples.

        :return: list of (id, persistent_object) tuples
        """
        return [(item_id, obj) for item_id, obj in self.collection.items()]

    def get_by_id(self, item_id: int):
        """
        Retrieve a single item by its ID.

        :param item_id: integer ID
        :return: the persistent object, or None if not found
        """
        return self.collection.get(item_id)

    def create(self, obj) -> int:
        """
        Add a new persistent object to the collection.

        :param obj: a Durus Persistent instance
        :return: the assigned ID
        """
        item_id = self._next_id()
        self.collection[item_id] = obj
        self.db.commit()
        return item_id

    def update(self, item_id: int, obj) -> bool:
        """
        Replace the object at the given ID.

        :param item_id: integer ID of the item to replace
        :param obj: the updated persistent object
        :return: True if the item existed and was replaced
        """
        if item_id not in self.collection:
            return False
        self.collection[item_id] = obj
        self.db.commit()
        return True

    def delete(self, item_id: int) -> bool:
        """
        Remove an item from the collection.

        :param item_id: integer ID of the item to remove
        :return: True if the item existed and was removed
        """
        if item_id not in self.collection:
            return False
        del self.collection[item_id]
        self.db.commit()
        return True
