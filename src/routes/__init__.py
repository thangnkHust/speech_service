from src.controllers.auth_controller import LoginResource, RegisterResource
from src.controllers.admin import UserListResource, UserResource
from src.controllers.user import ProfileResource, SpeakerListResource

def initialize_routes(api):
    # auth
    api.add_resource(LoginResource, '/api/auth/login')
    api.add_resource(RegisterResource, '/api/auth/register')

    # admin
    api.add_resource(UserListResource, '/api/admin/users')
    api.add_resource(UserResource, '/api/admin/users/<int:id>')

    # user
    api.add_resource(ProfileResource, '/api/profile')
    api.add_resource(SpeakerListResource, '/api/speakers')
