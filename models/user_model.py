from migrations.database import db_session
from migrations.user_migration import User


class UserModel:

    def __init__(self):
        pass

    def create(self, user: User):
        try:
            db_session.add(user)
            db_session.commit()
            return True
        except:
            return False

    def delete(self, id):
        pass

    def all(self):
        return 'sam'

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return user

    def update(self, id):
        pass
