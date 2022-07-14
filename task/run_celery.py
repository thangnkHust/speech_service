from app_celery import celery
from src.manage import app
from task.celery_utils import init_celery

# from gevent import monkey
# monkey.patch_all(httplib=False)

# app = create_app()
init_celery(app, celery)
