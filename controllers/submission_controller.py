from migrations.submission_migration import Submission
from models.submission_model import SubmissionModel
from sqlalchemy import or_, and_, join


class SubmissionController:

    def __int__(self):
        pass

    def add(self, student_id, teacher, book_id, chapter_id, name, status, score):
        submission = Submission(student_id, teacher, book_id, chapter_id, name, status, score)
        submission_model = SubmissionModel()
        res = submission_model.create(submission)
        return res


