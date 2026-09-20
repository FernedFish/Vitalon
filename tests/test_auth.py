"""
Authentication flow tests.

Run with: python -m unittest discover -s tests -v
"""

import tempfile
import unittest
from pathlib import Path

from vitalon.data.repositories import UserRepository
from vitalon.services.auth import AuthService


class AuthServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        users_file = Path(self.temporary_directory.name) / "users.csv"
        self.auth_service = AuthService(UserRepository(users_file))

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_sign_up_then_login_returns_the_new_user(self) -> None:
        created_user = self.auth_service.sign_up(
            "  maria  ", "  Barangay San Isidro  ", "secure-pass"
        )

        logged_in_user = self.auth_service.login("maria", "secure-pass")

        self.assertEqual(created_user.username, "maria")
        self.assertEqual(created_user.barangay, "Barangay San Isidro")
        self.assertIsNotNone(logged_in_user)
        self.assertEqual(logged_in_user.username, "maria")
        self.assertEqual(logged_in_user.barangay, "Barangay San Isidro")
        self.assertNotEqual(created_user.password, "secure-pass")

    def test_login_rejects_an_invalid_password(self) -> None:
        self.auth_service.sign_up("maria", "San Isidro", "secure-pass")

        logged_in_user = self.auth_service.login("maria", "incorrect-pass")

        self.assertIsNone(logged_in_user)

    def test_sign_up_rejects_duplicate_username_case_insensitively(self) -> None:
        self.auth_service.sign_up("Maria", "San Isidro", "secure-pass")

        with self.assertRaisesRegex(ValueError, "already in use"):
            self.auth_service.sign_up("mArIa", "San Isidro", "another-pass")


if __name__ == "__main__":
    unittest.main()
