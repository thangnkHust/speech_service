from src.controllers.auth_controller import LoginResource, RegisterResource
from src.controllers.admin import UserListResource, UserResource, UserActiveResource, AdminSpeakerListResource, \
    AdminSpeakerResource, AdminAudioSampleListResource, AdminAudioSampleResource, AdminRecordListResource
from src.controllers.user import ProfileResource, SpeakerListResource, SpeakerResource, \
    AudioListResource, SpeakerIdentificationResource, RecordListResource, RecordProcessingResource

def initialize_routes(api):
    # auth
    api.add_resource(LoginResource, '/api/auth/login')
    api.add_resource(RegisterResource, '/api/auth/register')

    # admin
    api.add_resource(UserListResource, '/api/admin/users')
    api.add_resource(UserResource, '/api/admin/users/<int:id>')
    api.add_resource(UserActiveResource, '/api/admin/users/<int:id>/active')
    api.add_resource(AdminSpeakerListResource, '/api/admin/speakers')
    api.add_resource(AdminSpeakerResource, '/api/admin/speakers/<int:speaker_id>')
    api.add_resource(AdminAudioSampleListResource, '/api/admin/speakers/<int:speaker_id>/audios')
    api.add_resource(AdminAudioSampleResource, '/api/admin/speakers/<int:speaker_id>/audios/<int:audio_id>')
    api.add_resource(AdminRecordListResource, '/api/admin/records')

    # user
    api.add_resource(ProfileResource, '/api/profile')
    api.add_resource(SpeakerListResource, '/api/speakers')
    api.add_resource(SpeakerResource, '/api/speakers/<string:speaker_name>')
    api.add_resource(AudioListResource, '/api/speakers/<string:speaker_name>/audios')
    api.add_resource(SpeakerIdentificationResource, '/api/speaker-identification')
    api.add_resource(RecordListResource, '/api/records')
    api.add_resource(RecordProcessingResource, '/api/speech-recognition')
