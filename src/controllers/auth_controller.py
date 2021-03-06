from flask_restful import Resource
from flask import request
from flask_restful import reqparse
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from src.services import UserService
from .common.decorators import admin_required
from .common.base_controller import AdminResource

class LoginResource(Resource):
    @admin_required()
    def get(self):
        user_service = UserService()
        roles = user_service.get_all_role()

        return roles

    @swag_from('../docs/auth/login.yaml')
    def post(self):
        user_service = UserService()
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, case_sensitive=False, trim=True)
        parser.add_argument('password', type=str, required=True, case_sensitive=False)
        args = parser.parse_args()

        return user_service.login(args.email, args.password)


class RegisterResource(AdminResource):
    @swag_from('../docs/auth/register.yaml')
    def post(self):
        user_service = UserService()
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, case_sensitive=False, trim=True)
        parser.add_argument('password', type=str, required=True, case_sensitive=False)
        args = parser.parse_args()

        return user_service.register(args.email, args.password)
