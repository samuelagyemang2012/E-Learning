from migrations.database import db_session
from migrations.response_migration import Response


class ResponseModel:

    def __init__(self):
        pass

    def create(self, response: Response):
        db_session.add(response)
        db_session.commit()

    def delete(self, id):
        pass

    def all(self):
        return Response.query.all()

    def get(self, id):
        response = Response.query.filter_by(id=id).first()
        return response

    def update(self, id):
        pass
