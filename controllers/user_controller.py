from migrations.user_migration import User
from models.user_model import UserModel
from sqlalchemy import or_, and_
from flask_bcrypt import generate_password_hash, check_password_hash


class UserController:

    def __int__(self):
        pass

    def login(self, username, student_id, password):
        user = User.query.filter(
            or_(User.username == username, User.student_id == student_id)
            # and_(User.password == password)
        ).first()

        if user is not None:
            if user.student_id == student_id or user.username == username and check_password_hash(user.password,
                                                                                                  password):
                return user.id, user.role_id
            else:
                return False
        return False

    def register(self, username, student_id, password, name, role_id):
        password = generate_password_hash(password)
        user = User(username, student_id, name, password, role_id)
        user_model = UserModel()
        res = user_model.create(user)
        return res
