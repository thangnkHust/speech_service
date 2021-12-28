from src.models import User
from src.database import db

class UserDAO:
    def __init__(self) -> None:
        self.model = User

    def get_all(self):
        try:
            session = db.session
            users = session.query(self.model).all()

            return users
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_by_email(self, email):
        try:
            session = db.session
            user = session.query(self.model).filter_by(email=email).first()

            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_by_id(self, id):
        try:
            session = db.session
            user = session.query(self.model).filter_by(id=id).first()

            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def create_user(self, email, password, role, id=None, name=None):
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

    def update_user(self, id, name, is_active=True):
        try:
            session = db.session
            user = session.query(self.model).filter_by(id=id).first()
            user.name = name
            user.is_active = is_active
            session.commit()
            return user.serialize()

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete(self, id):
        try:
            session = db.session
            user = session.query(self.model).filter_by(id=id).first()
            session.delete(user)
            session.commit()
            return True

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
