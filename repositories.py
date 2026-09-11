from models import User
import csv

class UserRepository:

    def __init__(self, filename="users.csv"):
        self.filename = filename

    def add(self):
        with open(self.filename, 'a', newline="") as file:
            csv.writer(file).writerow(user.username, user.barangay, user.password)

    def authenticate(self):
        with open(self.filename, newline="") as file:
            for row in csv.DictReader(file):
                if row["username"] == username and row["password"] == password:
                    return User(row["username"], row["barangay"], row["password"])
        return None

class RecordRepository:

    def __init__(self, filename="records.csv"):
        self.filename = filename

    def add(self, record):
        with open(self.filename, "a", newline="") as file:
            csv.writer(file).writerow([
                record.date_created,
                record.username,
                record.barangay,
                record.temperature,
                record.blood_pressure,
                record.heart_rate,
                record.respiratory_rate,
                record.assess_status()
            ])

    def get_by_username(self, username):
        records = []
        with open(self.filename, newline="") as file:
            for row in csv.DictReader(file):
                if row["username"] == username:
                    records.append(row)
        return records