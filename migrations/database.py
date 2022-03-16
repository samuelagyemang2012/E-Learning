from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)  # 'sqlite:////tmp/test.db')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()

    from migrations import book_migration, chapter_migration, roles_migration, user_migration, submission_migration, \
        response_migration, comment_migration
    Base.metadata.create_all(bind=engine)
