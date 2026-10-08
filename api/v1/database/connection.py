"""
Durus database connection manager (singleton).

Manages the FileStorage and Connection lifecycle,
and initializes the root-level PersistentDict containers
for each entity collection.
"""

import os
import logging

from durus.file_storage import FileStorage
from durus.connection import Connection
from durus.persistent_dict import PersistentDict

# -- Suppress verbose Durus commit logging --
logging.getLogger("durus").setLevel(logging.WARNING)


class DatabaseConnection:
    """
    Singleton that holds the Durus FileStorage and Connection.

    Call get_instance() to obtain the shared connection.
    """

    _instance = None

    # -- Names of all root-level collections --
    # Add new collection names here when creating new entities.
    COLLECTIONS = [
        "cars",
        "motorcycles",
        "mechanics",
        "parts",
        "orders",
        "users",
    ]

    def __init__(self, db_path: str):
        """
        Open the database file and initialize collections.

        :param db_path: filesystem path for the Durus storage file
        """
        # -- Ensure the data directory exists --
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        # -- Open Durus file storage and connection --
        self.storage = FileStorage(db_path)
        self.connection = Connection(self.storage)
        self.root = self.connection.get_root()

        # -- Initialize each collection as a PersistentDict if missing --
        for name in self.COLLECTIONS:
            if name not in self.root:
                self.root[name] = PersistentDict()

        self.connection.commit()

    @classmethod
    def initialize(cls, db_path: str):
        """
        Create the singleton instance.

        :param db_path: filesystem path for the Durus storage file
        """
        if cls._instance is None:
            cls._instance = cls(db_path)

    @classmethod
    def get_instance(cls) -> "DatabaseConnection":
        """
        Return the shared DatabaseConnection instance.

        :raises RuntimeError: if initialize() has not been called yet
        """
        if cls._instance is None:
            raise RuntimeError("Database not initialized. Call DatabaseConnection.initialize() first.")
        return cls._instance

    def commit(self):
        """Persist all pending changes to disk."""
        self.connection.commit()

    def abort(self):
        """Discard all pending changes since the last commit."""
        self.connection.abort()

    def get_collection(self, name: str) -> PersistentDict:
        """
        Get a root-level collection by name.

        :param name: collection key (e.g. 'cars', 'users')
        :return: the PersistentDict for that collection
        """
        return self.root[name]

    def close(self):
        """Close the underlying file storage."""
        self.storage.close()
        DatabaseConnection._instance = None
