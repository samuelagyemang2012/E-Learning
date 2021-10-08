from sqlalchemy import Column, Integer, String, DateTime, func
from migrations.database import Base


class Submission(Base):
    __tablename__ = 'submissions'
    id = Column('id', Integer, primary_key=True)
    student_id = Column('student_id', String(100), nullable=True)
    teacher_id = Column('teacher_id', Integer)
    book_id = Column('book_id', Integer)
    chapter_id = Column('chapter_id', Integer)
    name = Column("name", String(100))
    status = Column('status', String(20))
    score = Column('score', String(10))
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(), server_onupdate=func.now(), nullable=True)

    def __init__(self, student_id, teacher_id, book_id, chapter_id, name, status, score):
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.book_id = book_id
        self.chapter_id = chapter_id
        self.name = name
        self.status = status
        self.score = score

    # def __repr__(self):
    #     return f'<user {self.name, self.role_id,}>'
