from flask import jsonify
import datetime
from flask_jwt_extended import create_access_token
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
        self.user_dao.create_user(id=1, email='admin@gmail.com', password='12345678', name='admin', role=role)
        print('Seeder user admin successfully!!!')

    def get_all_role(self):
        roles = self.role_dao.get_all()
        roles = [role.serialize() for role in roles]

        return roles, 200

    def get_all_user(self):
        users = self.user_dao.get_all()
        users = [user.serialize() for user in users]

        return users, 200

    def login(self, email, password):
        user = self.user_dao.get_by_email(email)
        auth = user.check_password(password)
        if not auth:
            return {'message': 'Unauthorized'}, 401

        print(user.role.id)
        expires = datetime.timedelta(days=10)
        claims = {'admin': user.role.role_type == 'admin'}
        access_token = create_access_token(identity=str(user.id), additional_claims=claims, fresh=True, expires_delta=expires)
        return {'token': access_token}, 200

    def register(self, email, password):
        user = self.user_dao.get_by_email(email)

        if user:
            return {'msg': 'Account already exists!!!'}, 409

        role = self.role_dao.get_by_type('user')
        self.user_dao.create_user(email=email, password=password, role=role)

        return {'msg': 'Register successfully!!!'}, 201

    def get_by_id(self, id):
        user = self.user_dao.get_by_id(id)

        if not user:
            return {
                'msg': 'Account not found!!!'
            }, 404

        return user.serialize()

    def update_user(self, id, name):
        user = self.user_dao.get_by_id(id=id)

        if not user:
            return {
                'msg': 'Account not found!!!'
            }, 404

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
            }
        return {
            'msg': 'Internal Error!!!'
        }
