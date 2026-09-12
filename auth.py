import hashlib
import hmac
import os

from models import User


class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def login(self, username: str, password: str) -> User | None:
        user = self.user_repository.find_user(username.strip())
        return user if user and self._verify_password(password, user.password) else None

    def sign_up(self, username: str, barangay: str, password: str) -> User:
        username, barangay = username.strip(), barangay.strip()
        if not username or not barangay:
            raise ValueError("Username and barangay are required.")
        if len(password) < 8:
            raise ValueError("Password must contain at least 8 characters.")
        if self.user_repository.find_user(username):
            raise ValueError("That username is already in use.")
        user = User(username, barangay, self._hash_password(password))
        self.user_repository.add_user(user)
        return user

    @staticmethod
    def _hash_password(password: str) -> str:
        salt = os.urandom(16).hex()
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 310_000).hex()
        return f"pbkdf2_sha256${salt}${digest}"

    @staticmethod
    def _verify_password(password: str, stored: str) -> bool:
        if not stored.startswith("pbkdf2_sha256$"):
            return hmac.compare_digest(password, stored)
        _, salt, expected = stored.split("$", 2)
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 310_000).hex()
        return hmac.compare_digest(actual, expected)
