from migrations.database import db_session
from migrations.submission_migration import Submission


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

    def get_student_submissions(self, id):
        student_submission = Submission.query.filter_by(student_id=id).all()
        return student_submission

    def update(self, id):
        pass

    # user.no_of_logins += 1
    # session.commit()
