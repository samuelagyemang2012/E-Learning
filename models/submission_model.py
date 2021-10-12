from migrations.database import db_session
from migrations.submission_migration import Submission
from migrations.book_migration import Book
from migrations.user_migration import User
from migrations.chapter_migration import Chapter
from migrations.roles_migration import Role
from sqlalchemy import or_, and_, join


class SubmissionModel:

    def __init__(self):
        pass

    def create(self, submission: Submission):
        try:
            db_session.add(submission)
            db_session.commit()
            return True
        except:
            return False

    def delete(self, id):
        pass

    def all(self):
        return Submission.query.all()

    def get(self, id):
        submission = Submission.query.filter_by(id=id).first()
        return submission

    def student_get_pending(self, user_id):
        pending = Submission.query. \
            join(User, Submission.student_id == User.id). \
            join(Book, Submission.book_id == Book.id). \
            join(Chapter, Submission.chapter_id == Chapter.id). \
            add_columns(Submission.teacher,
                        Book.name.label("b_name"),
                        Chapter.name.label("c_name"),
                        Submission.name.label("s_name"),
                        Submission.created_on). \
            filter(Submission.status == "pending"). \
            filter(User.id == user_id).all()
        return pending

    def student_get_checked(self, user_id):
        checked = Submission.query. \
            join(User, Submission.student_id == User.id). \
            join(Book, Submission.book_id == Book.id). \
            join(Chapter, Submission.chapter_id == Chapter.id). \
            add_columns(Submission.teacher,
                        Book.name.label("b_name"),
                        Chapter.name.label("c_name"),
                        Submission.name.label("s_name"),
                        Submission.score,
                        Submission.created_on). \
            filter(Submission.status == "checked"). \
            filter(User.id == user_id).all()
        return checked

    def teacher_get_pending(self, name):
        pending = Submission.query. \
            join(User, Submission.student_id == User.id). \
            join(Book, Submission.book_id == Book.id). \
            join(Chapter, Submission.chapter_id == Chapter.id). \
            add_columns(User.name.label("student"),
                        Book.name.label("b_name"),
                        Chapter.name.label("c_name"),
                        Submission.name.label("s_name"),
                        Submission.created_on). \
            filter(Submission.status == "pending"). \
            filter(Submission.teacher == name).all()
        return pending


def update(self, id):
    pass

# user.no_of_logins += 1
# session.commit()
