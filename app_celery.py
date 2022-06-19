from celery import Celery

celery = Celery(__name__, config_source='task.celery_config')
