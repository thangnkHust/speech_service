from src.controllers.auth_controller import LoginResource, RegisterResource
from src.controllers.admin import UserListResource, UserResource

def initialize_routes(api):
    api.add_resource(LoginResource, '/api/auth/login')
    api.add_resource(RegisterResource, '/api/auth/register')
    api.add_resource(UserListResource, '/api/admin/users')
    api.add_resource(UserResource, '/api/admin/users/<int:id>')
