from migrations.book_migration import Book
from models.book_model import BookModel
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
