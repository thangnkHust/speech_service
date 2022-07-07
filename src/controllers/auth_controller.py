from flask_restful import Resource
from flask_restful import reqparse
from flasgger import swag_from
from src.services import UserService
from .common.base_controller import AdminResource
from src.utils.check_connection import check_connection

class LoginResource(Resource):
    def get(self):
        return check_connection()

    @swag_from('../docs/auth/login.yaml')
    def post(self):
        user_service = UserService()
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, trim=True, location=['form', 'json'])
        parser.add_argument('password', type=str, required=True, location=['form', 'json'])
        args = parser.parse_args()

        return user_service.login(args.email, args.password)


class RegisterResource(AdminResource):
    @swag_from('../docs/auth/register.yaml')
    def post(self):
        user_service = UserService()
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, case_sensitive=False, trim=True, location=['form', 'json'])
        parser.add_argument('password', type=str, required=True, case_sensitive=False, location=['form', 'json'])
        parser.add_argument('name', type=str, required=True, case_sensitive=False, trim=True, location=['form', 'json'])
        args = parser.parse_args()

        return user_service.register(args.email, args.password, args.name)
