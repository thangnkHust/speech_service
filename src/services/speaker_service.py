import os
from flask import current_app
from nanoid import generate
from src.daos import UserDAO, SpeakerDAO, AudioSampleDAO
from src.utils.speaker_identification import get_feature_data, get_speaker_result

class SpeakerService:
    def __init__(self) -> None:
        self.speaker_dao = SpeakerDAO()
        self.user_dao = UserDAO()
        self.audio_sample_dao = AudioSampleDAO()

    def get_speaker_of_user(self, user_id):
        speakers = self.speaker_dao.get_by_user_id(user_id=user_id)
        speakers = [speaker.serialize() for speaker in speakers]

        return speakers, 200

    def create_speaker(self, user_id, name):
        user = self.user_dao.get_by_id(id=user_id)

        if self.speaker_dao.create_speaker(name=name, user=user):
            return {
                'msg': 'Create speaker successfully!!!'
            }, 201

        return {
            'msg': 'Server Internal Error!!!'
        }, 500

    def get_detail_speaker(self, user_id, speaker_name):
        speaker = self.speaker_dao.get_by_name(user_id=user_id, name=speaker_name)

        if not speaker:
            return {
                'message': 'Not found!!!'
            }, 404

        return speaker.serialize()

    def check_valid_speaker(self, user_id, speaker_name):
        return self.speaker_dao.get_by_name(user_id=user_id, name=speaker_name)


    def get_audio_of_speaker(self, user_id, speaker_name):
        speaker = self.check_valid_speaker(user_id=user_id, speaker_name=speaker_name)

        if not speaker:
            return {
                'message': 'Not found speaker!!!'
            }, 404

        audios = self.audio_sample_dao.get_by_speaker_id(speaker_id=speaker.id)
        audios = [audio.serialize() for audio in audios]

        return audios, 200

    def create_audio_of_speaker(self, user_id, speaker_name, audio_file):
        speaker = self.check_valid_speaker(user_id=user_id, speaker_name=speaker_name)

        if not speaker:
            return {
                'message': 'Not found speaker!!!'
            }, 404

        folder_path = os.path.join(current_app.config['AUDIO_SAMPLE_FOLDER'], str(speaker.id))

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        try:
            file_ext = os.path.splitext(audio_file.filename)[1]
            filename_random = generate() + file_ext
            path_save = os.path.join(folder_path, filename_random)
            # save file to server
            audio_file.save(path_save)

            # Get feature data of audio sample
            feature_data = get_feature_data(file_path=path_save)
            # save to database
            self.audio_sample_dao.create_audio_sample(name=audio_file.filename, path=path_save, speaker=speaker, feature_data=feature_data.tobytes())

            return {
                'message': 'Create audio sample successfully!!!'
            }, 201
        except Exception as e:
            # When exception => delete file
            os.remove(path_save)
            raise e

    def speaker_identification(self, user_id, audio_test):
        # Get all audio sample enroll
        enroll_list = []
        speakers = self.speaker_dao.get_by_user_id(user_id=user_id)
        for speaker in speakers:
            audios = speaker.audio_samples
            for audio in audios:
                data = {
                    'speaker': speaker,
                    'audio_data': audio.feature_data
                }
                enroll_list.append(data)

        # Get feature data of audio test
        feature_test = get_feature_data(audio_test)

        # get speaker
        correct_speaker, confidence = get_speaker_result(enroll_list, feature_test)
        if not correct_speaker:
            return {
                'message': 'Internal error!!!'
            }, 500

        if confidence < 0.6:
            return {
                'message': 'The server cannot identify the speaker'
            }, 400

        return {
            'speaker': correct_speaker.serialize(),
            'confidences': confidence
        }
