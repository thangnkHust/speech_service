from flask_restful import reqparse
import werkzeug
from flasgger import swag_from
from flask import send_file

from ..common.base_controller import AdminResource
from src.services import SpeakerService

class AdminSpeakerListResource(AdminResource):
    def get(self):
        speaker_service = SpeakerService()

        return speaker_service.get_all_speaker()


class AdminSpeakerResource(AdminResource):
    def get(self, speaker_id):
        pass

    def delete(self, speaker_id):
        speaker_service = SpeakerService()

        return speaker_service.admin_delete_speaker(speaker_id=speaker_id)


class AdminAudioSampleListResource(AdminResource):
    def get(self, speaker_id):
        speaker_service = SpeakerService()

        return speaker_service.get_audio_sample_by_speaker(speaker_id=speaker_id)

    def post(self, speaker_id):
        speaker_service = SpeakerService()
        parser = reqparse.RequestParser()
        parser.add_argument('audio_file', type=werkzeug.datastructures.FileStorage, required=True, location='files')
        args = parser.parse_args()

        return speaker_service.create_audio_by_speaker_id(speaker_id=speaker_id, audio_file=args.audio_file)


class AdminAudioSampleResource(AdminResource):
    def get(self, speaker_id, audio_id):
        speaker_service = SpeakerService()

        return speaker_service.get_audio_sample_by_id(speaker_id=speaker_id, audio_id=audio_id)

    def delete(self, speaker_id, audio_id):
        speaker_service = SpeakerService()

        return speaker_service.admin_delete_audio_sample(speaker_id=speaker_id, audio_id=audio_id)
