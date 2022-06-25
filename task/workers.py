import time
from celery.result import AsyncResult

from app_celery import celery

def get_status(task_id):
    return AsyncResult(task_id, app=celery)

@celery.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5}, track_started=True)
def speech_recognition(record_path: str):
    try:
        time.sleep(31*60)
        # Call core Speech recognition
        # Lay ket qua luu DB, export file .json
        # raise ValueError()

        return {
            'message': 'result.json'
        }
    except Exception as e:
        raise e
