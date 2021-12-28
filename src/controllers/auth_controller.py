from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from src.services import UserService
from .common.decorators import admin_required
from .common.base_controller import AdminResource

class LoginResource(Resource):
    @admin_required()
    def get(self):
        user_service = UserService()
        roles = user_service.get_all_role()

        return roles

    def post(self):
        user_service = UserService()
        data = request.form

        return user_service.login(data.get('email'), data.get('password'))


class RegisterResource(AdminResource):
    def post(self):
        user_service = UserService()
        data = request.form

        return user_service.register(data.get('email'), data.get('password'))
