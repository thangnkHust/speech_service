import json
import os
import time
import math
from celery.result import AsyncResult
from flask import current_app
from app_celery import celery
from pyannote.core import Segment
from pyannote.audio import Pipeline

from src.daos import RecordDAO, SpeakerDAO
from src.utils.constants import SUCCESS, FAILURE, TIME_PER_SPLIT
from src.utils.waveform import audio_load
from src.core.speaker_diarization import SpeakerDiarizationModel
from src.core.speaker_identification import SpeakerIdentificationModel
from src.core.speech_to_text import SpeechToTextModel


def get_status(task_id):
    return AsyncResult(task_id, app=celery)

@celery.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 1, 'countdown': 5}, track_started=True)
def speech_recognition(record_path: str, user_id: int, record_id: str):
    record_dao_worker = RecordDAO()
    try:
        # storage data to json file
        record_name = os.path.basename(record_path)
        result_name = os.path.splitext(record_name)[0]
        folder_result = current_app.config['RESULT_FOLDER']
        result_path = f'{folder_result}/{result_name}.json'

        # Call core Speech recognition
        result, duration, handle_time = handle_speech_recognition(user_id, record_path)

        result_json = {
            'record_id': record_id,
            'record_name': record_name,
            'duration': duration,
            'time_per_segment': TIME_PER_SPLIT,
            'device': SpeechToTextModel.device,
            'process_time': round(handle_time, 2),
            'data': result
        }

        # Storage to server and update in DB
        with open(result_path, 'w', encoding='utf8') as f:
            json.dump(result_json, f, ensure_ascii=False, indent=2, separators=(',', ': '))

        record_dao_worker.update_record(record_id=record_id, user_id=user_id, status=SUCCESS, result_path=result_path)

        return {
            'result_path': result_path
        }
    except Exception as e:
        record_dao_worker.update_record(record_id=record_id, user_id=user_id, status=FAILURE, result_path=None)
        os.remove(result_path)
        raise e


def handle_speech_recognition(user_id, input_file):
    duration = audio_load.get_duration(input_file)
    temp = math.ceil(duration/TIME_PER_SPLIT)
    start = time.time()
    print(f'debug_{temp}')

    enroll_list = []
    speaker_dao = SpeakerDAO()
    speakers = speaker_dao.get_by_user_id(user_id=user_id)
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
        print(f'debug_handle {i}')
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

    return result, duration, handle_time
