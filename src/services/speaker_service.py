from flask import jsonify
import datetime
from src.daos import SpeakerDAO
from src.daos import UserDAO

class SpeakerService:
    def __init__(self) -> None:
        self.speaker_dao = SpeakerDAO()
        self.user_dao = UserDAO()

    def get_speaker_of_user(self, user_id):
        speakers = self.speaker_dao.get_by_user_id(user_id=user_id)
        speakers = [speaker.serialize() for speaker in speakers]

        return speakers, 200

    def create_speaker(self, user_id, name):
        user = self.user_dao.get_by_id(id=user_id)
        print(name)

        if self.speaker_dao.create_speaker(name=name, user=user):
            return {
                'msg': 'Create speaker successfully!!!'
            }, 201

        return {
            'msg': 'Server Internal Error!!!'
        }, 500
