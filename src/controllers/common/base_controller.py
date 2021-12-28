from flask_restful import Resource
from .decorators import admin_required

class AdminResource(Resource):
    method_decorators = [admin_required()]
