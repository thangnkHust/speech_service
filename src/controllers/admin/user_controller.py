from flask_restful import Resource
from flask import request
from src.services import UserService
from ..common.base_controller import AdminResource

class UserListResource(AdminResource):
    def get(self):
        user_service = UserService()
        users = user_service.get_all_user()

        return users

class UserResource(AdminResource):
    def get(self, id):
        user_service = UserService()
        user = user_service.get_by_id(id)

        return user

    def put(self, id):
        data = request.form
        user_service = UserService()

        return user_service.update_user(id, name=data.get('name'))

    def delete(self, id):
        user_service = UserService()

        return user_service.delete_user(id=id)
