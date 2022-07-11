import os
from flask import current_app, jsonify, send_file
from nanoid import generate
from src.daos import UserDAO, SpeakerDAO, AudioSampleDAO
from src.core.speaker_identification import get_feature_data, get_speaker_result

class SpeakerService:
    def __init__(self) -> None:
        self.speaker_dao = SpeakerDAO()
        self.user_dao = UserDAO()
        self.audio_sample_dao = AudioSampleDAO()

    '''
    Logic for user
    '''
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

    def delete_speaker(self, user_id, speaker_name):
        speaker = self.speaker_dao.get_by_name(user_id=user_id, name=speaker_name)

        if not speaker:
            return {
                'message': 'Bad request!!!'
            }, 400

        if self.speaker_dao.delete_speaker(speaker=speaker):
            return {
                'message': 'Delete speaker successfully'
            }, 200

        return {
            'message': 'Server Internal Error!!!'
        }, 500

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
            print(path_save)

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
            response = jsonify({
                'message': 'Internal error!!!'
            })
            response.status_code = 500

        if confidence < 0.6:
            response = jsonify({
                'message': 'The server cannot identify the speaker'
            })
            response.status_code = 400

        response = jsonify({
            'speaker': correct_speaker.serialize(),
            'confidences': confidence
        })
        response.status_code = 200

        return response


    '''
    Logic for admin
    '''
    def get_all_speaker(self):
        speakers = self.speaker_dao.get_all()
        data = []
        for spk in speakers:
            temp = spk.serialize()
            temp['user'] = spk.user.email
            data.append(temp)

        res = jsonify(data)
        res.status_code = 200

        return res


    def admin_delete_speaker(self, speaker_id: int):
        speaker = self.speaker_dao.get_by_id(id=speaker_id)
        if not speaker:
            res = jsonify({
                'message': 'Bad request!!!'
            })
            res.status_code = 400
        else:
            self.speaker_dao.delete_speaker(speaker=speaker)
            res = jsonify({
                'message': 'Delete speaker successfully!!!'
            })
            res.status_code = 200

        return res

    def get_audio_sample_by_speaker(self, speaker_id: int):
        speaker = self.speaker_dao.get_by_id(id=speaker_id)
        if not speaker:
            return {'message': 'Speaker not found!!!'}, 404
        list_audio = self.audio_sample_dao.get_by_speaker_id(speaker_id=speaker.id)
        return [audio.serialize() for audio in list_audio]

    def create_audio_by_speaker_id(self, speaker_id: int, audio_file):
        speaker = self.speaker_dao.get_by_id(id=speaker_id)
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

        pass

    def get_audio_sample_by_id(self, speaker_id, audio_id):
        # speaker = self.speaker_dao.get_by_id(id=speaker_id)
        # if not speaker:
        #     return {'message': 'Audio sample not found!!!'}, 404

        audio = self.audio_sample_dao.get_by_audio_id(speaker_id=speaker_id, audio_id=audio_id)
        if not audio:
            return {'message': 'Audio sample not found!!!'}, 404

        # with open(audio.path, 'rb') as f:
        #     content = f.read()
        # return content
        return send_file(
                f"/app/{audio.path}",
                mimetype="audio/wav",
                as_attachment=True,
                # attachment_filename="test.wav"
            )

    def admin_delete_audio_sample(self, speaker_id: int, audio_id: int):
        audio = self.audio_sample_dao.get_by_audio_id(speaker_id=speaker_id, audio_id=audio_id)
        if not audio:
            return {'message': 'Audio sample not found!!!'}, 404

        if self.audio_sample_dao.delete_audio_sample(audio_sample=audio):
            os.remove(audio.path)
            return {'message': 'Delete audio sample successfully!!!'}, 200

        return {'message': 'Server Internal Error!!!'}, 500
