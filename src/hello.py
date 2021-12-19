from flask_restful import Resource
from src.models.role import Role
from src.models.user import User
from src.database import db

class Hello(Resource):
    def get(self):
        res = {}

        return res
