import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from src.config import config_dict, FLASK_ENV
from src.database import initialize_db
from src.routes import initialize_routes

def create_app(flask_env=FLASK_ENV):
    app = Flask(__name__)
    CORS(app)

    # Config app
    app.config.from_object(config_dict[flask_env])
    app.app_context().push()

    # Init database
    initialize_db(app)

    Bcrypt(app)
    JWTManager(app)

    # Init router
    api = Api(app)
    initialize_routes(api)

    return app

app = create_app()
