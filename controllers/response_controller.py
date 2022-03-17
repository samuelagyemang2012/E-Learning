from migrations.response_migration import Response
from migrations.user_migration import User
from models.response_model import ResponseModel
from datetime import datetime


# datetime.strptime("2013-1-25", '%Y-%m-%d').strftime('%m/%d/%y')


class ResponseController:

    def __int__(self):
        pass

    def add_response(self, comment_id, user_id, response):
        response = Response(comment_id, user_id, response)
        response_model = ResponseModel()
        response_model.create(response)
        res = response.query.filter_by(comment_id=comment_id).first()
        return res.id

    def get_responses(self, comment_id):
        responses = Response.query. \
            join(User, Response.user_id == User.id). \
            add_columns(User.name.label("name"),
                        Response.response.label("response"),
                        Response.created_on.label("created_on")
                        ). \
            filter(Response.comment_id == comment_id).all()
        return responses
