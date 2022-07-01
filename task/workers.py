import json
import os
import time
from celery.result import AsyncResult
from flask import current_app

from app_celery import celery
from src.daos import RecordDAO
from src.utils.constants import SUCCESS, FAILURE


def get_status(task_id):
    return AsyncResult(task_id, app=celery)

@celery.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5}, track_started=True)
def speech_recognition(record_path: str, user_id: int, record_id: str):
    try:
        time.sleep(3*60)

        # fake data from template
        with(open('.docker/data/result/template_result.json', 'r')) as f:
            result_json = json.load(f)
            result_json['record_id'] = record_id

        # storage data to json file
        result_name = os.path.splitext(os.path.basename(record_path))[0]
        folder_result = current_app.config['RESULT_FOLDER']
        result_path = f'{folder_result}/{result_name}.json'

        with open(result_path, 'w', encoding='utf8') as f:
            json.dump(result_json, f, ensure_ascii=False, indent=2, separators=(',', ': '))

        record_dao = RecordDAO()
        record_dao.update_record(record_id=record_id, user_id=user_id, status=SUCCESS, result_path=result_path)

        # Call core Speech recognition
        # Lay ket qua luu DB, export file .json

        return {
            'result_path': result_path
        }
    except Exception as e:
        record_dao.update_record(record_id=record_id, user_id=user_id, status=FAILURE, result_path=None)
        raise e
