from sqlalchemy import Column, Integer, String, DateTime, func
from migrations.database import Base


class Response(Base):
    __tablename__ = 'responses'
    id = Column('id', Integer, primary_key=True)
    comment_id = Column('comment_id', Integer)
    user_id = Column('user_id', Integer)
    response = Column('response', String(500), nullable=False)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), server_onupdate=func.now(), nullable=True)
    deleted_on = Column(String(250), nullable=True)

    def __init__(self, comment_id, user_id, response):
        self.comment_id = comment_id
        self.user_id = user_id
        self.response = response

    # def __repr__(self):
    #     return f'<response {self.name!r}>'
