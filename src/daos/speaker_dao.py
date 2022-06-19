from src.models import Speaker
from src.database import db

class SpeakerDAO:
    def __init__(self) -> None:
        self.model = Speaker

    def get_all(self):
        try:
            session = db.session
            speaker = session.query(self.model).all()

            return speaker
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_by_user_id(self, user_id):
        try:
            session = db.session
            speakers = session.query(self.model).filter_by(user_id=user_id)

            return speakers
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_by_name(self, user_id, name):
        try:
            session = db.session
            speaker = session.query(self.model).filter_by(name=name, user_id=user_id).first()

            return speaker
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def create_speaker(self, name, user):
        try:
            session = db.session
            speaker = self.model(name=name, user=user)
            session.add(speaker)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_speaker(self, speaker):
        try:
            session = db.session
            session.delete(speaker)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
