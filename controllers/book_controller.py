from migrations.book_migration import Book
from migrations.chapter_migration import Chapter
from models.book_model import BookModel
from models.chapter_model import ChapterModel
from sqlalchemy import or_, and_


class BookController:

    def __int__(self):
        pass

    def add_book(self, title):
        book = Book(title)
        book_model = BookModel()
        book_model.create(book)
        res = Book.query.filter_by(name=title).first()
        return res.id

    def get_chapters(self, book_id):
        chapters = Chapter.query.filter_by(book_id=book_id).all()
        return chapters
