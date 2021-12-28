from flask import request
from flask_restful import reqparse
from ..common.base_controller import BaseResource
from src.services import SpeakerService

class SpeakerListResource(BaseResource):
    def get(self, user_data):
        speaker_service = SpeakerService()

        return speaker_service.get_speaker_of_user(user_id=user_data['user_id'])

    def post(self, user_data):
        speaker_service = SpeakerService()
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()

        return speaker_service.create_speaker(user_id=user_data['user_id'], name=args['name'])
