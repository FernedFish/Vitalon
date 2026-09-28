from statistics import mean
import json


def print_dashboard(records: list[dict[str, str]]) -> None:
    if not records:
        print("\nNo readings yet. Log your first vital signs to see your dashboard.")
        return
    latest = records[0]
    print("\n=== Health Dashboard ===")
    print(f"Latest reading: {latest['date_created']} — {latest['status']}")
    print(f"Temperature: {latest['temperature']} °C | BP: {latest['blood_pressure']} mmHg")
    print(f"Heart rate: {latest['heart_rate']} bpm | Oxygen: {latest['oxygen_saturation']}%")
    print(f"Respiratory rate: {latest['respiratory_rate']} breaths/min | BMI: {latest.get('bmi') or '—'}")
    _print_trends(records)


def print_history(records: list[dict[str, str]]) -> None:
    if not records:
        print("\nNo health history yet.")
        return
    print("\n=== Recent Health History ===")
    for row in records[:10]:
        print(f"{row['date_created']} | {row['status']:<15} | {row['temperature']} °C | BP {row['blood_pressure']} | HR {row['heart_rate']} | O₂ {row['oxygen_saturation']}% | BMI {row['bmi']}")


def print_search_results(records: list[dict[str, str]], vital_type: str | None = None) -> None:
    if not records:
        print("\nNo records match those filters.")
        return

    labels = {
        "temperature": ("Temperature", "°C"),
        "blood_pressure": ("Blood pressure", "mmHg"),
        "heart_rate": ("Heart rate", "bpm"),
        "oxygen_saturation": ("Oxygen", "%"),
        "respiratory_rate": ("Respiratory rate", "breaths/min"),
        "bmi": ("BMI", ""),
        "blood_glucose": ("Glucose", "mg/dL"),
    }
    print("\n=== Search Results ===")
    for number, record in enumerate(records, start=1):
        if vital_type:
            label, unit = labels[vital_type]
            measurement = f"{label} {record.get(vital_type, '—')} {unit}".rstrip()
        else:
            measurement = f"BP {record['blood_pressure']} | HR {record['heart_rate']} | O₂ {record['oxygen_saturation']}%"
        print(f"[{number}] {record['date_created']} | {record['status']:<15} | {measurement}")


def print_record_details(record: dict[str, str]) -> None:
    print("\n=== Health Record Details ===")
    print(f"Date: {record['date_created']} | Status: {record['status']}")
    print(f"Temperature: {record['temperature']} °C | Blood pressure: {record['blood_pressure']} mmHg")
    print(f"Heart rate: {record['heart_rate']} bpm | Oxygen: {record['oxygen_saturation']}%")
    print(f"Respiratory rate: {record['respiratory_rate']} breaths/min")
    print(f"BMI: {record.get('bmi') or '—'} | Blood glucose: {record.get('blood_glucose') or '—'} mg/dL")
    print(f"Symptoms/notes: {record.get('symptoms') or '—'}")
    print(f"Chronic conditions: {record.get('chronic_conditions') or '—'}")
    print(f"Symptom severity: {record.get('symptom_severity') or '—'}")
    print("Alerts:")
    try:
        alerts = json.loads(record.get("alerts", "[]"))
    except json.JSONDecodeError:
        alerts = []
    if alerts:
        for alert in alerts:
            print(f"- {alert}")
    else:
        print("- No saved alerts for this record.")


def _print_trends(records: list[dict[str, str]]) -> None:
    recent = records[:7]
    if len(recent) < 2:
        print("Trend: add another reading to compare changes.")
        return
    print("\n7-reading trend (latest vs. earlier):")
    for label, key, unit in [("Temperature", "temperature", "°C"), ("Heart rate", "heart_rate", "bpm"), ("Oxygen", "oxygen_saturation", "%")]:
        values = [float(row[key]) for row in recent if row.get(key)]
        change = values[0] - values[-1]
        arrow = "↑" if change > 0 else "↓" if change < 0 else "→"
        print(f"{label}: {mean(values):.1f} {unit} average {arrow} {abs(change):.1f} from earliest")
