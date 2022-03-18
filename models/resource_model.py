from migrations.database import db_session
from migrations.resource_migration import Resource
from migrations.user_migration import User
from sqlalchemy import or_, and_, join


class ResourceModel:

    def __init__(self):
        pass

    def create(self, resource: Resource):
        try:
            db_session.add(resource)
            db_session.commit()
            return True
        except:
            return False

    def update_downloads(self, resource_id, new_downloads):
        resource = Resource.query.filter_by(resource_id=resource_id).first()
        resource.downloads = new_downloads
        db_session.commit()

    def delete(self, id):
        pass

    def get(self, rid):
        resource = Resource.query.filter_by(resource_id=rid).first()
        return resource

    def get_resources(self):
        resources = Resource.query. \
            join(User, Resource.user_id == User.id). \
            add_columns(Resource.name.label("r_name"),
                        Resource.description.label("desc"),
                        Resource.resource_id.label("resource_id"),
                        Resource.downloads.label("downloads"),
                        User.name.label("u_name"),
                        Resource.created_on). \
            filter().all()
        return resources

    # def all(self):
    #     return Resource.query.all()

    #
    # def get_by_name(self, sub_name):
    #     submission = Submission.query.filter_by(name=sub_name).first()
    #     return submission
    #
    # def student_get_pending(self, user_id):
    #     pending = Submission.query. \
    #         join(User, Submission.student_id == User.id). \
    #         join(Book, Submission.book_id == Book.id). \
    #         join(Chapter, Submission.chapter_id == Chapter.id). \
    #         add_columns(Submission.teacher,
    #                     Book.name.label("b_name"),
    #                     Chapter.name.label("c_name"),
    #                     Submission.name.label("s_name"),
    #                     Submission.created_on). \
    #         filter(Submission.status == "pending"). \
    #         filter(User.id == user_id).all()
    #     return pending
    #
    # def student_get_checked(self, user_id):
    #     checked = Submission.query. \
    #         join(User, Submission.student_id == User.id). \
    #         join(Book, Submission.book_id == Book.id). \
    #         join(Chapter, Submission.chapter_id == Chapter.id). \
    #         add_columns(Submission.teacher,
    #                     Book.name.label("b_name"),
    #                     Chapter.name.label("c_name"),
    #                     Submission.name.label("s_name"),
    #                     Submission.score,
    #                     Submission.created_on). \
    #         filter(Submission.status == "checked"). \
    #         filter(User.id == user_id).all()
    #     return checked
    #
    # def teacher_get_pending(self, name):
    #     pending = Submission.query. \
    #         join(User, Submission.student_id == User.id). \
    #         join(Book, Submission.book_id == Book.id). \
    #         join(Chapter, Submission.chapter_id == Chapter.id). \
    #         add_columns(User.name.label("student"),
    #                     Book.name.label("b_name"),
    #                     Chapter.id.label("c_id"),
    #                     Chapter.name.label("c_name"),
    #                     Submission.id.label("s_id"),
    #                     Submission.name.label("s_name"),
    #                     Submission.created_on). \
    #         filter(Submission.status == "pending"). \
    #         filter(Submission.teacher == name).all()
    #     return pending
    #
    # def get_student_submissions_by_book(self, user_id, book_id):
    #     submissions = Submission.query. \
    #         join(User, Submission.student_id == user_id). \
    #         join(Chapter, Submission.chapter_id == Chapter.id). \
    #         add_columns(Chapter.name.label("cname"),
    #                     Submission.score.label("score"),
    #                     Submission.updated_on.label("updated_on")
    #                     ). \
    #         filter(Submission.book_id == book_id).all()
    #     return submissions
    #
    # def update(self, name, status, score):
    #     submission = Submission.query.filter_by(name=name).first()
    #     submission.status = status
    #     submission.score = score
    #     # db_session.add(submission)
    #     db_session.commit()

# user.no_of_logins += 1
# session.commit()
