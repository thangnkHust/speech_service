from flask import request
from flasgger import swag_from
from ..common.base_controller import BaseResource
from src.services import UserService

class ProfileResource(BaseResource):
    @swag_from('../../docs/user/get_profile.yaml')
    def get(self, user_data):
        user_service = UserService()
        user = user_service.get_by_id(user_data.get('user_id'))

        return user

    @swag_from('../../docs/user/update_profile.yaml')
    def put(self, user_data):
        data = request.form
        user_service = UserService()
        user = user_service.update_profile(id=user_data.get('user_id'), name=data.get('name'))

        return user
