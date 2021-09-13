from migrations.database import db_session
from migrations.roles_migration import Role


class RoleModel:

    def __init__(self):
        pass

    def create(self, role: Role):
        db_session.add(role)
        db_session.commit()

    def delete(self, id):
        pass

    def all(self):
        return 'sam'

    def get(self, id):
        user = Role.query.filter_by(id=id).first()
        return user

    def update(self, id):
        pass
