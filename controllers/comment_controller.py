from migrations.comment_migration import Comment
from models.comment_model import CommentModel
from models.chapter_model import ChapterModel
from sqlalchemy import or_, and_


class CommentController:

    def __int__(self):
        pass

    def add_comment(self, user_id, comment):
        comment = Comment(user_id, comment)
        comment_model = CommentModel()
        comment_model.create(comment)
        res = Comment.query.filter_by(user_id=user_id).first()
        return res.id

    def get_posts(self):
        posts = Comment.query.filter_by().all()
        return posts
