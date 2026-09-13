from dataclasses import asdict, dataclass, field
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
    systolic: int
    diastolic: int
    heart_rate: int
    respiratory_rate: int
    oxygen_saturation: int
    age : int = 0
    sex : str = "" 
    is_pregnant : bool = False
    chronic_conditions: str = ""
    sypmtoms_severity: str = "None"
    weight_kg: float | None = None
    height_cm: float | None = None
    blood_glucose: float | None = None
    symptoms: str = ""
    date_created: str = field(default_factory=lambda: date.today().isoformat())
    status: str = ""

    @property
    def blood_pressure(self) -> str:
        return f"{self.systolic}/{self.diastolic}"

    @property
    def bmi(self) -> float | None:
        if not self.weight_kg or not self.height_cm:
            return None
        return round(self.weight_kg / ((self.height_cm / 100) ** 2), 1)

    def to_row(self) -> dict[str, object]:
        row = asdict(self)
        row["blood_pressure"] = self.blood_pressure
        row["bmi"] = self.bmi if self.bmi is not None else ""
        return row
