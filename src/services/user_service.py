from email import message
from flask import jsonify
import datetime
from flask_jwt_extended import create_access_token
import os
from src.daos import RoleDAO
from src.daos import UserDAO

class UserService:
    def __init__(self) -> None:
        self.role_dao = RoleDAO()
        self.user_dao = UserDAO()

    def seed_role(self):
        roles = [
            {
                'id': 1,
                'type': 'admin'
            },
            {
                'id': 2,
                'type': 'user'
            }
        ]
        for role in roles:
            self.role_dao.create_role(id=role['id'], role_type=role['type'])
        print('Seeder role successfully!!!')

    def seed_user(self):
        role = self.role_dao.get_by_type('admin')
        self.user_dao.create_user(email=os.getenv('EMAIL_ADMIN', 'admin@gmail.com'), password=os.getenv('PASSWORD_ADMIN', '12345678'), name='admin', role=role)
        print('Seeder user admin successfully!!!')

    def get_all_role(self):
        roles = self.role_dao.get_all()
        roles = [role.serialize() for role in roles]

        return roles, 200


    def get_all_user(self):
        users = self.user_dao.get_all()
        users_formatted = []

        for user in users:
            user_formatted = user.serialize()
            user_formatted['role'] = user.role.role_type
            users_formatted.append(user_formatted)

        res = jsonify(users_formatted)
        res.status_code = 200

        return res


    def change_active(self, id: int):
        user = self.user_dao.get_by_id(id=id)
        if not user:
            res = jsonify({
                'message': 'User not found!'
            })
            res.status_code = 404
        else:
            if self.user_dao.change_active(id=id):
                res = jsonify({
                    'message': 'Change active successfully'
                })
                res.status_code = 200
            else:
                res = jsonify({
                    'message': 'Server Internal Error!!!'
                })
                res.status_code = 500

        return res


    def login(self, email, password):
        user = self.user_dao.get_by_email(email)
        if not user:
            return {'message': 'Unauthorized'}, 401

        auth = user.check_password(password)
        if not auth:
            return {'message': 'Unauthorized'}, 401

        expires = datetime.timedelta(days=10)
        claims = {'admin': user.role.role_type == 'admin'}
        access_token = create_access_token(identity=str(user.id), additional_claims=claims, fresh=True, expires_delta=expires)
        res = jsonify({
            'token': access_token,
            'admin': user.role.role_type == 'admin'
        })
        res.status_code = 200
        return res

    def register(self, email, password, name):
        user = self.user_dao.get_by_email(email)

        if user:
            return {'msg': 'Account already exists!!!'}, 409

        role = self.role_dao.get_by_type('user')
        self.user_dao.create_user(email=email, password=password, name=name, role=role)

        return {'msg': 'Register successfully!!!'}, 201

    def get_by_id(self, id):
        user = self.user_dao.get_by_id(id)

        if not user:
            return {
                'msg': 'Account not found!!!'
            }, 404

        return user.serialize()

    def update_user(self, id, name, is_active=True):
        user = self.user_dao.get_by_id(id=id)

        if not user:
            return {
                'msg': 'Account not found!!!'
            }, 404
        return self.user_dao.update_user(id=id, name=name, is_active=is_active)

    def update_profile(self, id, name):
        user = self.user_dao.get_by_id(id=id)

        if not user:
            return {
                'msg': 'Account not found!!!'
            }, 404

        if not user.is_active:
            return {
                'msg': 'Account has been blocked!!!'
            }, 400

        return self.user_dao.update_user(id=id, name=name)

    def delete_user(self, id):
        user = self.user_dao.get_by_id(id=id)

        if not user:
            return {
                'msg': 'Account not found!!!'
            }, 404

        status = self.user_dao.delete(id=id)
        if status:
            return {
                'msg': 'Delete successfully!!!'
            }, 200
        return {
            'msg': 'Internal Error!!!'
        }, 500
