import imp
import time
from app_celery import celery

@celery.task
def create_task():
    time.sleep(10)
    return 'Success'
