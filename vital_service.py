from models import HealthRecord


class VitalService:
    """Assesses readings using simple screening thresholds, not a diagnosis."""

    @staticmethod
    def assess_vitals(record: HealthRecord) -> tuple[str, list[str]]:
        alerts: list[str] = []
        urgent = False

        severity = record.symptom_severity.strip().capitalize()
        if severity == "Severe":
            alerts.append("Severe symptoms reported: requires immediate medical attention.")
            urgent = True
        elif severity == "Moderate":
            alerts.append("Moderate symptoms reported: monitor closely and consult a healthcare provider.")

        # --- Temperature Check ---
        if record.temperature >= 39 or record.temperature < 35:
            alerts.append("Temperature is in an urgent range.")
            urgent = True
        elif record.temperature >= 38:
            alerts.append("Fever detected.")

        # --- Blood Pressure Check (Adjusted for Pregnancy) ---
        if record.systolic >= 180 or record.diastolic >= 120:
            alerts.append("Blood pressure is in a crisis range.")
            urgent = True
        elif record.is_pregnant and (record.systolic >= 140 or record.diastolic >= 90):
            alerts.append("Elevated blood pressure during pregnancy detected (preeclampsia risk).")
            urgent = True
        elif record.systolic >= 140 or record.diastolic >= 90:
            alerts.append("Blood pressure is high.")
        elif record.systolic < 90 or record.diastolic < 60:
            alerts.append("Blood pressure is low.")

        # --- Heart Rate Check ---
        if record.heart_rate > 120 or record.heart_rate < 45:
            alerts.append("Heart rate is in an urgent range.")
            urgent = True
        elif record.heart_rate > 100 or record.heart_rate < 60:
            alerts.append("Heart rate is outside the usual resting range.")

        # --- Oxygen Saturation Check ---
        if record.oxygen_saturation < 90:
            alerts.append("Oxygen saturation is in an urgent range.")
            urgent = True
        elif record.oxygen_saturation < 95:
            alerts.append("Oxygen saturation is below the usual range.")

        # --- Respiratory Rate Check ---
        if record.respiratory_rate < 12 or record.respiratory_rate > 20:
            alerts.append("Respiratory rate is outside the usual adult resting range.")

        # --- Contextual Risk Factor Notes ---
        if record.chronic_conditions and alerts:
            alerts.append(f"Patient has pre-existing condition(s): {record.chronic_conditions}.")

        if record.age >= 65 and alerts:
            alerts.append("Higher vulnerability risk due to age (65+).")

        if urgent:
            return "Urgent", alerts
        if alerts:
            return "Needs attention", alerts
        return "Normal", ["All entered readings are within the tracker's usual ranges."]
