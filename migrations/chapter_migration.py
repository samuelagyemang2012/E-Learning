from sqlalchemy import Column, Integer, String, DateTime, func
from migrations.database import Base


class Chapter(Base):
    __tablename__ = 'chapters'
    id = Column('id', Integer, primary_key=True)
    book_id = Column('book_id', Integer, nullable=False)
    name = Column('name', String(100), nullable=False, unique=True)
    path = Column('path', String(100), nullable=False)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), server_onupdate=func.now(), nullable=True)
    deleted_on = Column(String(250), nullable=True)

    def __init__(self, book_id, name, path):
        self.book_id = book_id
        self.name = name
        self.path = path

    def __repr__(self):
        return f'<chapter {self.name!r}>'
