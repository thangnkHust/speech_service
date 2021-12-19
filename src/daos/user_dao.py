from src.models import User
from src.database import db

class UserDAO:
    def __init__(self) -> None:
        self.model = User

    def get_all(self):
        pass

    def create_user(self, email, password, name, role, id=None):
        try:
            session = db.session
            user = self.model(id=id, email=email, password=password, name=name, role=role)
            user.hash_password()
            session.add(user)
            session.commit()

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
