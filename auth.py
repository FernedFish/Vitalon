from models import User

class AuthService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def login(self, username, password):
        return self.user_repository.find_user(username, password)

    def sign_up(self, username, barangay, password):
        user = User(username, barangay, password)
        self.user_repository.add_user(user)
        return user