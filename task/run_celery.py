from app_celery import celery
from src.manage import app
from task.celery_utils import init_celery

# app = create_app()
init_celery(app, celery)
