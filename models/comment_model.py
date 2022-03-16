from migrations.database import db_session
from migrations.comment_migration import Comment


class CommentModel:

    def __init__(self):
        pass

    def create(self, comment: Comment):
        db_session.add(comment)
        db_session.commit()

    def delete(self, id):
        pass

    def all(self):
        return Comment.query.all()

    def get(self, id):
        comment = Comment.query.filter_by(id=id).first()
        return comment

    def update(self, id):
        pass
