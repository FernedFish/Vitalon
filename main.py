from repositories import UserRepository, RecordRepository
from models import User, HealthRecord
import menu
from auth import AuthService

class Vitalon:

    def __init__(self):
        self.current_user = None
        self.user_repository = UserRepository()
        self.record_repository = RecordRepository()
        self.auth_service = AuthService(self.user_repository)
        self.current_user = None


    def run(self):
        while(True):
            self.show_mainmenu()