"""
User model module.

Represents a system user for simple username/password authentication.
Passwords are stored as SHA-256 hashes, never in plain text.
"""

import hashlib

from durus.persistent import Persistent


class User(Persistent):
    """A system user with hashed password authentication."""

    def __init__(self, username="", password="", role="user"):
        self.username = username
        # -- Store the password as a SHA-256 hash --
        self.password_hash = self._hash_password(password)
        self.role = role

    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Hash a plain-text password using SHA-256.

        :param password: plain-text password
        :return: hexadecimal hash string
        """
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def check_password(self, password: str) -> bool:
        """
        Verify a plain-text password against the stored hash.

        :param password: plain-text password to verify
        :return: True if the password matches
        """
        return self.password_hash == self._hash_password(password)

    def to_dict(self) -> dict:
        """Serialize the user to a plain dictionary (excludes password)."""
        return {
            "username": self.username,
            "role": self.role,
        }
