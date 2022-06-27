from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, jwt_required
from src.daos import UserDAO

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request(fresh=True)
            claims = get_jwt()

            if not claims['admin']:
                return {'msg': 'Permission denied'}, 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper

def user_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request(fresh=True)
            claims = get_jwt()
            user_data = {
                'user_id': claims['sub'],
            }

            user_dao = UserDAO()
            user = user_dao.get_by_id(claims['sub'])

            if not user.is_active:
                return {
                    'message': 'Account has been blocked!!!'
                }, 400

            if claims['admin']:
                return {'msg': 'Permission denied'}, 403
            return fn(user_data, *args, **kwargs)

        return decorator

    return wrapper
