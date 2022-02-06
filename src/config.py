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
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret key')
    BUNDLE_ERRORS = True
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
    # MONGODB_SETTINGS = {
    #     'host': 'mongodb://{}:{}@{}:{}/{}'.format(
    #         DB_USERNAME,
    #         DB_PASSWORD,
    #         DB_HOST,
    #         DB_PORT,
    #         DB_NAME
    #     )
    # }

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUDIO_SAMPLE_FOLDER = '.docker/data/audio_sample'
    SWAGGER = {
        'title': "Speech Searvice API",
        'uiversion': 3
    }

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config_dict = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
