from src.models import Role
from src.database import db

class RoleDAO:
    def __init__(self) -> None:
        self.model = Role

    def get_all(self):
        return db.session.query(self.model).all()

    def get_by_type(self, role_type):
        try:
            session = db.session
            role = session.query(self.model).filter_by(role_type=role_type).first()

            return role
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def create_role(self, id, role_type):
        try:
            session = db.session
            role = self.model(id=id, role_type=role_type)
            session.add(role)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
