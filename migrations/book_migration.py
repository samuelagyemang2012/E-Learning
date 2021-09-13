from sqlalchemy import Column, Integer, String, DateTime, func
from migrations.database import Base


class Book(Base):
    __tablename__ = 'books'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(100), nullable=False, unique=True)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), server_onupdate=func.now(), nullable=True)
    deleted_on = Column(String(250), nullable=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<book {self.name!r}>'
