from migrations.database import db_session
from migrations.book_migration import Book


class BookModel:

    def __init__(self):
        pass

    def create(self, book: Book):
        db_session.add(book)
        db_session.commit()

    def delete(self, id):
        pass

    def all(self):
        return Book.query.all()

    def get(self, id):
        user = Book.query.filter_by(id=id).first()
        return user

    def update(self, id):
        pass
