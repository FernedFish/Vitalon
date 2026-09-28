import tempfile
import unittest
from datetime import date
from pathlib import Path

from vitalon.data.repositories import RecordRepository
from vitalon.models import HealthRecord


def make_record(username: str, created: str, status: str, glucose: float | None = None) -> HealthRecord:
    return HealthRecord(
        username=username, barangay="San Isidro", temperature=36.8,
        systolic=120, diastolic=80, heart_rate=72, respiratory_rate=16,
        oxygen_saturation=98, blood_glucose=glucose, date_created=created, status=status,
    )


class HistorySearchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.repository = RecordRepository(Path(self.temporary_directory.name) / "records.csv")
        self.repository.add(make_record("maria", "2026-09-01", "Normal"), ["All readings normal."])
        self.repository.add(make_record("maria", "2026-09-15", "Urgent", 180), ["Blood pressure is in a crisis range."])
        self.repository.add(make_record("juan", "2026-09-15", "Urgent", 180), [])

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_filters_by_date_and_status_for_the_current_user(self) -> None:
        records = self.repository.search_by_username(
            "maria", date(2026, 9, 10), date(2026, 9, 15), "Urgent"
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["username"], "maria")
        self.assertEqual(records[0]["date_created"], "2026-09-15")

    def test_vital_filter_keeps_only_records_with_that_optional_value(self) -> None:
        records = self.repository.search_by_username("maria", vital_type="blood_glucose")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["blood_glucose"], "180")

    def test_alerts_are_saved_with_the_record(self) -> None:
        record = self.repository.get_by_username("maria")[0]
        self.assertIn("Blood pressure", record["alerts"])


if __name__ == "__main__":
    unittest.main()
