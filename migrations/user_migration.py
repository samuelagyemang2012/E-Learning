from sqlalchemy import Column, Integer, String, DateTime, func
from migrations.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    student_id = Column('student_id', String(100), nullable=True)
    username = Column('username', String(100), nullable=True)
    name = Column('name', String(250), nullable=False)
    password = Column('password', String(250), nullable=False)
    role_id = Column('role_id', Integer)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), server_onupdate=func.now(), nullable=True)

    def __init__(self, username, student_id, name, password, role_id):
        self.username = username
        self.student_id = student_id
        self.name = name
        self.password = password
        self.role_id = role_id

    # def __repr__(self):
    #     return f'<user {self.name, self.role_id,}>'
