# from flask import jsonify, make_response
from src.daos import RoleDAO
from src.daos import UserDAO

class UserService:
    def __init__(self) -> None:
        self.role_dao = RoleDAO()
        self.user_dao = UserDAO()

    def get_all_role(self):
        roles = self.role_dao.get_all()
        res = []
        for role in roles:
            res.append(role.serialize())

        return res

    def login(self):
        pass

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
