class Menu:
    @staticmethod
    def show_main_menu() -> None:
        print("\n=== Vitalon: Health Tracker ===")
        print("[1] Log in\n[2] Sign up\n[3] Reset password\n[0] Exit")

    @staticmethod
    def show_user_menu(username: str) -> None:
        print(f"\n=== {username}'s Health Tracker ===")
        print("[1] Log vital signs\n[2] View dashboard\n[3] View health history\n[9] Delete account\n[0] Log out")
