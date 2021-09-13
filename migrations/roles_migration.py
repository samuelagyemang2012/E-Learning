from sqlalchemy import Column, Integer, String, DateTime, func
from migrations.database import Base


class Role(Base):
    __tablename__ = 'roles'
    id = Column('id', Integer, primary_key=True)
    role = Column('role', String(100), nullable=False, unique=True)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), server_onupdate=func.now(), nullable=True)
    deleted_on = Column(String(250), nullable=True)

    def __init__(self, role):
        self.role = role

    def __repr__(self):
        return '<role %r>' % self.role
