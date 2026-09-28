import csv
import json
from datetime import date
from pathlib import Path

from ..models import HealthRecord, User

USER_FIELDS = ["username", "barangay", "password"]
RECORD_FIELDS = [
    "date_created", "username", "barangay", "age", "sex", "is_pregnant",
    "chronic_conditions", "symptom_severity", "temperature", "blood_pressure",
    "systolic", "diastolic", "heart_rate", "respiratory_rate",
    "oxygen_saturation", "weight_kg", "height_cm", "bmi", "blood_glucose",
    "symptoms", "status", "alerts",
]


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

    def update_user(self, updated_user: User) -> None:
        if not self.filename.exists():
            return
        
        with self.filename.open(newline="", encoding="utf-8") as file:
            users = list(csv.DictReader(file))
            
        for row in users:
            if row["username"].casefold() == updated_user.username.casefold():
                row["password"] = updated_user.password
                break
                
        with self.filename.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=USER_FIELDS)
            writer.writeheader()
            writer.writerows(users)

    def delete_user(self, username: str) -> None:
        if not self.filename.exists():
            return
            
        with self.filename.open(newline="", encoding="utf-8") as file:
            users = [row for row in csv.DictReader(file) if row["username"].casefold() != username.casefold()]
            
        with self.filename.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=USER_FIELDS)
            writer.writeheader()
            writer.writerows(users)

    def _ensure_file(self) -> None:
        if not self.filename.exists() or self.filename.stat().st_size == 0:
            with self.filename.open("w", newline="", encoding="utf-8") as file:
                csv.DictWriter(file, fieldnames=USER_FIELDS).writeheader()


class RecordRepository:
    def __init__(self, filename="records.csv"):
        self.filename = Path(filename)

    def add(self, record: HealthRecord, alerts: list[str] | None = None) -> None:
        self._ensure_file()
        row = record.to_row()
        row["alerts"] = json.dumps(alerts or [])
        with self.filename.open("a", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=RECORD_FIELDS).writerow(row)

    def get_by_username(self, username: str) -> list[dict[str, str]]:
        if not self.filename.exists():
            return []
        with self.filename.open(newline="", encoding="utf-8") as file:
            rows = [row for row in csv.DictReader(file) if row["username"].casefold() == username.casefold()]
        return sorted(rows, key=lambda row: row["date_created"], reverse=True)

    def search_by_username(
        self,
        username: str,
        start_date: date | None = None,
        end_date: date | None = None,
        status: str | None = None,
        vital_type: str | None = None,
    ) -> list[dict[str, str]]:
        """Return one user's records matching optional search criteria.

        A vital-type search returns records that contain a value for that vital.
        This is especially useful for optional BMI and blood-glucose readings.
        """
        records = self.get_by_username(username)
        matches: list[dict[str, str]] = []
        for record in records:
            record_date = date.fromisoformat(record["date_created"])
            if start_date and record_date < start_date:
                continue
            if end_date and record_date > end_date:
                continue
            if status and record.get("status") != status:
                continue
            if vital_type and not record.get(vital_type):
                continue
            matches.append(record)
        return matches

    def _ensure_file(self) -> None:
        if not self.filename.exists() or self.filename.stat().st_size == 0:
            with self.filename.open("w", newline="", encoding="utf-8") as file:
                csv.DictWriter(file, fieldnames=RECORD_FIELDS).writeheader()
            return

        # Add the alerts column to records created before this feature existed.
        with self.filename.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames == RECORD_FIELDS:
                return
            rows = list(reader)
        with self.filename.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=RECORD_FIELDS)
            writer.writeheader()
            for row in rows:
                row.setdefault("alerts", "[]")
                writer.writerow(row)

    def delete_by_username(self, username: str) -> None:
        if not self.filename.exists():
            return
            
        with self.filename.open(newline="", encoding="utf-8") as file:
            records = [row for row in csv.DictReader(file) if row["username"].casefold() != username.casefold()]
            
        with self.filename.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=RECORD_FIELDS)
            writer.writeheader()
            writer.writerows(records)
