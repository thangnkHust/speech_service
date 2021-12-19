from src.controllers import LoginController

def initialize_routes(api):
    api.add_resource(LoginController, '/api/auth/login')
