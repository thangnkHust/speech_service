from flask_restful import reqparse
from flask import jsonify
import werkzeug
from flasgger import swag_from

from ..common.base_controller import BaseResource
from src.services import SpeakerService
from task.workers import create_task, get_job

class SpeakerListResource(BaseResource):
    @swag_from('../../docs/speaker/get_speaker_user.yaml')
    def get(self, user_data):
        speaker_service = SpeakerService()

        return speaker_service.get_speaker_of_user(user_id=user_data['user_id'])

    @swag_from('../../docs/speaker/create_speaker.yaml')
    def post(self, user_data):
        speaker_service = SpeakerService()
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument('name', type=str, required=True, case_sensitive=False)
        args = parser.parse_args()

        return speaker_service.create_speaker(user_id=user_data['user_id'], name=args['name'])


class SpeakerResource(BaseResource):
    @swag_from('../../docs/speaker/get_detail_speaker.yaml')
    def get(self, user_data, speaker_name):
        speaker_service = SpeakerService()

        return speaker_service.get_detail_speaker(user_id=user_data['user_id'], speaker_name=speaker_name)

    def delete(self, user_data, speaker_name):
        speaker_service = SpeakerService()

        return speaker_service.delete_speaker(user_id=user_data['user_id'], speaker_name=speaker_name)

class AudioListResource(BaseResource):
    @swag_from('../../docs/audio_sample/get_audio_speaker.yaml')
    def get(self, user_data, speaker_name):
        speaker_service = SpeakerService()

        return speaker_service.get_audio_of_speaker(user_id=user_data['user_id'], speaker_name=speaker_name)

    def post(self, user_data, speaker_name):
        speaker_service = SpeakerService()
        parser = reqparse.RequestParser()
        parser.add_argument('audio_file', type=werkzeug.datastructures.FileStorage, required=True, location='files')
        args = parser.parse_args()

        return speaker_service.create_audio_of_speaker(user_id=user_data['user_id'], speaker_name=speaker_name, audio_file=args.audio_file)

class SpeakerIdentificationResource(BaseResource):
    @swag_from('../../docs/speaker/speaker_identification.yaml')
    def post(self, user_data):
        speaker_service = SpeakerService()
        parser = reqparse.RequestParser()
        parser.add_argument('audio_file', type=werkzeug.datastructures.FileStorage, required=True, location='files')
        args = parser.parse_args()
        # res = jsonify({'file': args.audio_file.mimetype})
        # res.status_code = 201

        return speaker_service.speaker_identification(user_id=user_data['user_id'], audio_test=args.audio_file)
