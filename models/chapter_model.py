from migrations.database import db_session
from migrations.chapter_migration import Chapter


class ChapterModel:

    def __init__(self):
        pass

    def create(self, chapter: Chapter):
        db_session.add(chapter)
        db_session.commit()

    def delete(self, id):
        pass

    def all(self):
        return 'sam'

    def get(self, id):
        chapter = Chapter.query.filter_by(id=id).first()
        return chapter

    def update(self, id):
        pass
