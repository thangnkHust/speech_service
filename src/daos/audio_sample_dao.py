from src.models import AudioSample
from src.database import db

class AudioSampleDAO:
    def __init__(self) -> None:
        self.model = AudioSample

    def get_by_speaker_id(self, speaker_id):
        try:
            session = db.session
            audios = session.query(self.model).filter_by(speaker_id=speaker_id)

            return audios
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def create_audio_sample(self, name, path, feature_data, speaker):
        try:
            session = db.session
            audio = self.model(name=name, path=path, feature_data=feature_data, speaker=speaker)
            session.add(audio)
            session.commit()

            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
