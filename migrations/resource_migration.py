from sqlalchemy import Column, Integer, String, DateTime, func
from migrations.database import Base


class Resource(Base):
    __tablename__ = 'resources'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', String(100), nullable=False)
    name = Column('name', String(200))
    resource_id = Column('resource_id', String(200))
    description = Column('description', String(500))
    downloads = Column("downloads", Integer, default=0)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), server_onupdate=func.now(), nullable=True)

    def __init__(self, user_id, name, resource_id, description):
        self.user_id = user_id
        self.name = name
        self.resource_id = resource_id
        self.description = description
        # self.downloads = downloads

    # def __repr__(self):
    #     return f'<user {self.name, self.role_id,}>'
