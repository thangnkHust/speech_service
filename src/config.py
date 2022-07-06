import os

env = os.getenv('ENV', 'dev').lower()
if env in ['prod', 'production']:
    FLASK_ENV = 'prod'
elif env in ['dev', 'development']:
    FLASK_ENV = 'dev'
else:
    FLASK_ENV = env

class Config():
    APP_ROOTDIR = os.path.abspath(os.path.dirname(__file__))
    # Config jwt key
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret key')
    # return only one error validate field (form request)
    BUNDLE_ERRORS = True
    # Config DB
    DB_USERNAME = os.getenv('DB_USERNAME', 'missing_db_username')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'missing_db_password')
    DB_HOST = os.getenv('DB_HOST', 'missing_db_host')
    DB_PORT = os.getenv('DB_PORT', 'missing_db_port')
    DB_NAME = os.getenv('DB_NAME', 'missing_db_name')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
        DB_USERNAME,
        DB_PASSWORD,
        DB_HOST,
        DB_PORT,
        DB_NAME
    )
    # Config data folder
    AUDIO_SAMPLE_FOLDER = '.docker/data/audio_sample'
    RECORD_FOLDER = '.docker/data/record'
    RESULT_FOLDER = '.docker/data/result'
    SWAGGER = {
        'title': "Speech Searvice API",
        'uiversion': 3
    }
    # Config for celery queue management
    CELERY_CONFIG = {
        'broker_url': os.getenv('RABBIT_URL', 'missing_broker_url'),
        'result_backend': os.getenv('REDIS_URL', 'missing_redis_url')
    }

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    FLASK_APP = 'app_flask'
    ENV = 'development'
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    TESTING = False

config_dict = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
