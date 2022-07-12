from src.daos import SpeakerDAO
from flask_restful import reqparse
from flask_restful import Resource
import werkzeug
import math
import time
from pyannote.core import Segment
# from flasgger import swag_from

from ..common.base_controller import BaseResource
from src.services import RecordService
from src.utils.check_connection import *
from src.core.speaker_diarization import SpeakerDiarizationModel
from src.core.speaker_identification import SpeakerIdentificationModel
from src.core.speech_to_text import SpeechToTextModel
from src.utils.waveform import audio_load
from src.utils.constants import TIME_PER_SPLIT, DEVICE

class RecordListResource(BaseResource):
    def get(self):
        return check_connection()

    def post(self, user_data):
        """Upload record

        Args:
            user_data (dict): contain user_id get by token

        Returns:
            Status Upload
        """
        parser = reqparse.RequestParser()
        parser.add_argument('record_file', type=werkzeug.datastructures.FileStorage, required=True, location='files')
        args = parser.parse_args()
        record_service = RecordService()

        return record_service.upload_record(user_id=user_data['user_id'], record_file=args['record_file'])

class RecordProcessingResource(BaseResource):
    # def get(self):
    #     return check_connection()
    def get(self, user_data):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument('task_id', type=str, required=True, location='args')
        args = parser.parse_args()
        record_service = RecordService()

        return record_service.get_processing_info(task_id=args['task_id'])


    def post(self, user_data):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument('record_id', type=str, required=True)
        args = parser.parse_args()
        record_service = RecordService()

        return record_service.request_processing(user_id=user_data['user_id'], record_id=args['record_id'])

class RecordTranscriptResource(BaseResource):
    def get(self, user_data):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument('record_id', type=str, required=True, location='args')
        args = parser.parse_args()
        record_service = RecordService()

        return record_service.get_full_transcript(user_id=user_data['user_id'], record_id=args['record_id'])


class TestResource(BaseResource):
    def post(self, user_data):
        input_file = ".docker/data/_5K9_3Wi6i_0.wav"
        duration = audio_load.get_duration(input_file)
        temp = math.ceil(duration/TIME_PER_SPLIT)

        start = time.time()

        enroll_list = []
        speaker_dao = SpeakerDAO()
        speakers = speaker_dao.get_by_user_id(user_id=user_data['user_id'])
        for speaker in speakers:
            audios = speaker.audio_samples
            for audio in audios:
                data = {
                    'speaker': speaker,
                    'audio_data': audio.feature_data
                }
                enroll_list.append(data)
        result_temp = []
        for i in range(temp):
            start_time = i*TIME_PER_SPLIT
            if i == temp-1:
                end_time = duration
            else:
                end_time = (i+1)*TIME_PER_SPLIT
            result_diarization = SpeakerDiarizationModel.speaker_diarization(input_file, start_time, end_time)
        
            for spk in result_diarization:
                excerpt = Segment(start=spk['segment']['start'], end=spk['segment']['end'])
                waveform, _ = audio_load.crop(input_file, excerpt)
                spk['speaker'] =  SpeakerIdentificationModel.speaker_identification(enroll_list, waveform.squeeze().numpy())

            result_temp.append(result_diarization)

        result = [result_temp[0][0]]
        for i in range(len(result_temp)):
            for j in range(len(result_temp[i])):
                if i != len(result_temp) - 1:
                    if j == 0 and result[len(result)-1] and result[len(result)-1]['speaker']['name'] == result_temp[i][j]['speaker']['name']:
                        result[len(result)-1]['segment']['end'] = result_temp[i][j]['segment']['end']
                    else:
                        result.append(result_temp[i][j])
                elif len(result) != 1:
                    result.append(result_temp[i][j])

        for item in result:
            item['transcript'], item['reliability_transcript'], item['transcript_info'] = SpeechToTextModel.speech_to_text(input_file, item['segment']['start'], item['segment']['end'])
        end = time.time()
        handle_time = end - start

        return jsonify(result)
