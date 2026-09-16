from auth import AuthService
from dashboard import print_dashboard, print_history
from menu import Menu
from models import HealthRecord
from repositories import RecordRepository, UserRepository
from vital_service import VitalService


class Vitalon:
    def __init__(self):
        self.user_repository = UserRepository()
        self.record_repository = RecordRepository()
        self.auth_service = AuthService(self.user_repository)
        self.current_user = None

    def run(self) -> None:
        while True:
            Menu.show_main_menu()
            choice = input("Choose an option: ").strip()
            if choice == "1": self._login()
            elif choice == "2": self._sign_up()
            elif choice == "9": self.reser_password()
            elif choice == "0":
                
                print("Take care. Goodbye!"); return
            else: print("Please choose a listed option.")

    def _sign_up(self) -> None:
        try:
            self.current_user = self.auth_service.sign_up(input("Username: "), input("Barangay: "), input("Password (8+ characters): "))
            print(f"Account created. Welcome, {self.current_user.username}!")
            self._user_session()
        except ValueError as error: print(f"Could not create account: {error}")

    def _login(self) -> None:
        self.current_user = self.auth_service.login(input("Username: "), input("Password: "))
        if not self.current_user:
            print("Invalid username or password."); return
        print(f"Welcome back, {self.current_user.username}!")
        self._user_session()

    def _user_session(self) -> None:
        while self.current_user:
            Menu.show_user_menu(self.current_user.username)
            choice = input("Choose an option: ").strip()
            if choice == "1": self._log_vitals()
            elif choice == "2": print_dashboard(self.record_repository.get_by_username(self.current_user.username))
            elif choice == "3": print_history(self.record_repository.get_by_username(self.current_user.username))
            elif choice == "9":
                if self.delete_account():
                    self.current_user = None
            elif choice == "0": self.current_user = None
            else: print("Please choose a listed option.")

    def _log_vitals(self) -> None:
        try:
            # Demographics & Clinical Context
            age = self._number("Age: ", int, 0, 130)
            sex = input("Sex (Male/Female/Other): ").strip()
            
            is_pregnant = False
            if sex.casefold() in ("female", "f"):
                preg_input = input("Are you currently pregnant? (y/n): ").strip().casefold()
                is_pregnant = preg_input in ("y", "yes")

            chronic_conditions = input("Chronic conditions (e.g., Hypertension, Diabetes, or leave empty): ").strip()

            print("Symptom severity options: [1] None  [2] Mild  [3] Moderate  [4] Severe")
            severity_map = {"1": "None", "2": "Mild", "3": "Moderate", "4": "Severe"}
            severity_choice = input("Select symptom severity (1-4, default 1): ").strip()
            symptom_severity = severity_map.get(severity_choice, "None")

            record = HealthRecord(
                username=self.current_user.username,
                barangay=self.current_user.barangay,
                age=age,
                sex=sex,
                is_pregnant=is_pregnant,
                chronic_conditions=chronic_conditions,
                symptom_severity=symptom_severity,
                temperature=self._number("Temperature (°C): ", float, 30, 45),
                systolic=self._number("Systolic blood pressure: ", int, 50, 250),
                diastolic=self._number("Diastolic blood pressure: ", int, 30, 150),
                heart_rate=self._number("Heart rate (bpm): ", int, 25, 250),
                respiratory_rate=self._number("Respiratory rate (breaths/min): ", int, 5, 80),
                oxygen_saturation=self._number("Oxygen saturation (%): ", int, 50, 100),
                weight_kg=self._optional_number("Weight (kg, optional): ", float, 1, 500),
                height_cm=self._optional_number("Height (cm, optional): ", float, 30, 300),
                blood_glucose=self._optional_number("Blood glucose (mg/dL, optional): ", float, 10, 1000),
                symptoms=input("Symptoms or notes (optional): ").strip(),
            )
            record.status, alerts = VitalService.assess_vitals(record)
            self.record_repository.add(record)
            print(f"\nSaved. Status: {record.status}")
            for alert in alerts:
                print(f"- {alert}")
            if record.status == "Urgent":
                print("Seek emergency care now, especially if there are severe symptoms. This tracker is not a diagnosis.")
        except ValueError as error:
            print(f"Reading was not saved: {error}")

    @staticmethod
    def _number(prompt: str, kind, minimum: float, maximum: float):
        value = kind(input(prompt))
        if not minimum <= value <= maximum: raise ValueError(f"Enter a value from {minimum} to {maximum}.")
        return value

    @staticmethod
    def _optional_number(prompt: str, kind, minimum: float, maximum: float):
        text = input(prompt).strip()
        if not text: return None
        value = kind(text)
        if not minimum <= value <= maximum: raise ValueError(f"Enter a value from {minimum} to {maximum}.")
        return value

    def _reset_password(self) -> None:
        try:
            self.auth_service.reset_password(
                input("Username: "),
                input("Verify Barangay: "),
                input("New Password (8+ characters): ")
            )
            print("Password reset successfully. You can now log in.")
        except ValueError as error: 
            print(f"Reset failed: {error}")

    def _delete_account(self) -> bool:
        print("\nWARNING: This will permanently delete your account and all health records.")
        confirm = input("Type 'DELETE' to confirm: ")
        if confirm != "DELETE":
            print("Account deletion cancelled.")
            return False
            
        try:
            self.auth_service.delete_account(
                self.current_user.username, 
                input("Enter password to verify: ")
            )
            self.record_repository.delete_by_username(self.current_user.username)
            print("Account and all associated records deleted.")
            return True
        except ValueError as error:
            print(f"Deletion failed: {error}")
            return False


if __name__ == "__main__":
    Vitalon().run()
