from src.services import UserService

class Seed:
    def __init__(self) -> None:
        self.user_service = UserService()

    def seed_user_role(self) -> None:
        self.user_service.seed_role()
        self.user_service.seed_user()
