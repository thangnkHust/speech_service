from flask_restful import Resource
from src.services import UserService

class LoginController(Resource):
    def get(self):
        user_service = UserService()
        return user_service.get_all_role()
