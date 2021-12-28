from flask_restful import Resource
from .decorators import admin_required, user_required

class AdminResource(Resource):
    method_decorators = [admin_required()]

class BaseResource(Resource):
    method_decorators = [user_required()]
