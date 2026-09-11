from dataclasses import dataclass
from datetime import date

@dataclass
class User:
    username: str
    barangay: str
    password: str


@dataclass
class HealthRecord:
    username: str
    barangay: str
    temperature: float
    blood_pressure: str
    heart_rate: int
    respiratory_rate: int
    date_created: str = date.today().isoformat()
