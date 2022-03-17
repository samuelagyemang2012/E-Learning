from migrations.comment_migration import Comment
from migrations.user_migration import User
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

    def get_user_posts(self, user_id):
        comments = Comment.query.filter_by(user_id=user_id).all()
        return comments

    def get_posts(self):
        comments = Comment.query. \
            join(User, Comment.user_id == User.id). \
            add_columns(Comment.id.label("id"),
                        User.name.label("name"),
                        Comment.comment.label("comment"),
                        Comment.created_on.label("created_on")
                        ). \
            filter().all()
        return comments

    def get_post(self, cid):
        post = Comment.query.filter_by(id=cid).first()
        return post
