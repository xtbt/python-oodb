"""
User repository module.

Handles persistence operations for User entities,
including lookup by username for authentication.
"""

from api.v1.database.repository import BaseRepository


class UserRepository(BaseRepository):
    """Repository for User objects, stored in the 'users' collection."""

    collection_name = "users"

    def find_by_username(self, username: str):
        """
        Search for a user by username.

        :param username: the username to look up
        :return: (user_id, User) tuple if found, or (None, None)
        """
        for user_id, user in self.collection.items():
            if user.username == username:
                return user_id, user
        return None, None
