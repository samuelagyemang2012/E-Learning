from sqlalchemy import Column, Integer, String, DateTime, func
from migrations.database import Base


class Comment(Base):
    __tablename__ = 'comments'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    chapter_id = Column('chapter_id', Integer)
    comment = Column('comment', String(500), nullable=False)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), server_onupdate=func.now(), nullable=True)
    deleted_on = Column(String(250), nullable=True)

    def __init__(self, user_id, chapter_id, comment):
        self.user_id = user_id
        self.chapter_id = chapter_id
        self.comment = comment

    # def __repr__(self):
    #     return f'<comment {self.name!r}>'
