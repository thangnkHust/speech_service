import imp
import time
from celery.result import AsyncResult

from app_celery import celery

def get_job(job_id):
    return AsyncResult(job_id, app=celery)

@celery.task
def create_task():
    time.sleep(20)
    return 10
