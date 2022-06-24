from typing import List
from src.models import Record, User
from src.database import db
from src.utils.constants import PENDING

class RecordDAO:
    def __init__(self) -> None:
        self.model = Record

    def get_all(self) -> List[Record]:
        try:
            session = db.session
            records = session.query(self.model).all()

            return records
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


    def create_record(self, id: str, user: User, record_path: str, status:int=PENDING) -> str:
        try:
            session = db.session
            record = self.model(id=id, user=user, record_path=record_path, status=status)
            session.add(record)
            session.commit()

            return record.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


    def get_by_record_id(self, record_id: int, user_id: int) -> Record:
        try:
            session = db.session
            record = session.query(self.model).filter_by(id=record_id, user_id=user_id).first()

            return record
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


    def update_record(self, record_id: str, user_id: int, status: int, result_path: str=None):
        try:
            session = db.session
            record = session.query(self.model).filter_by(id=record_id, user_id=user_id).first()
            record.status = status
            record.result_path = result_path
            session.commit()

            return record.serialize()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
