import csv
from pathlib import Path

from models import HealthRecord, User

USER_FIELDS = ["username", "barangay", "password"]
RECORD_FIELDS = ["date_created", "username", "barangay", "age", "sex", "is+pregannt", "chronic_conditions", "symptoms_severity" "temperature", "blood_pressure", "systolic", "diastolic", "heart_rate", "respiratory_rate", "oxygen_saturation", "weight_kg", "height_cm", "bmi", "blood_glucose", "symptoms", "status"]


class UserRepository:
    def __init__(self, filename="users.csv"):
        self.filename = Path(filename)

    def add_user(self, user: User) -> None:
        self._ensure_file()
        with self.filename.open("a", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=USER_FIELDS).writerow({"username": user.username, "barangay": user.barangay, "password": user.password})

    def find_user(self, username: str) -> User | None:
        if not self.filename.exists():
            return None
        with self.filename.open(newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                if row["username"].casefold() == username.casefold():
                    return User(row["username"], row["barangay"], row["password"])
        return None

    def _ensure_file(self) -> None:
        if not self.filename.exists() or self.filename.stat().st_size == 0:
            with self.filename.open("w", newline="", encoding="utf-8") as file:
                csv.DictWriter(file, fieldnames=USER_FIELDS).writeheader()


class RecordRepository:
    def __init__(self, filename="records.csv"):
        self.filename = Path(filename)

    def add(self, record: HealthRecord) -> None:
        self._ensure_file()
        with self.filename.open("a", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=RECORD_FIELDS).writerow(record.to_row())

    def get_by_username(self, username: str) -> list[dict[str, str]]:
        if not self.filename.exists():
            return []
        with self.filename.open(newline="", encoding="utf-8") as file:
            rows = [row for row in csv.DictReader(file) if row["username"].casefold() == username.casefold()]
        return sorted(rows, key=lambda row: row["date_created"], reverse=True)

    def _ensure_file(self) -> None:
        if not self.filename.exists() or self.filename.stat().st_size == 0:
            with self.filename.open("w", newline="", encoding="utf-8") as file:
                csv.DictWriter(file, fieldnames=RECORD_FIELDS).writeheader()
