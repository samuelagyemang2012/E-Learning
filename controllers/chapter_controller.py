from migrations.chapter_migration import Chapter
from models.chapter_model import ChapterModel
from sqlalchemy import or_, and_


class ChapterController:

    def __int__(self):
        pass

    def add_chapter(self, book_id, name, path):
        try:
            chapter = Chapter(book_id, name, path)
            chapter_model = ChapterModel()
            chapter_model.create(chapter)
            return True
        except:
            return False
