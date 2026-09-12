from statistics import mean


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
        print(f"{row['date_created']} | {row['status']:<15} | {row['temperature']} °C | BP {row['blood_pressure']} | HR {row['heart_rate']} | O₂ {row['oxygen_saturation']}%")


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
