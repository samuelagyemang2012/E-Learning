from migrations.database import init_db, db_session
from models.user_model import User, UserModel
from models.book_model import Book, BookModel
from models.roles_model import Role, RoleModel
from models.chapter_model import Chapter, ChapterModel
from models.submission_model import Submission, SubmissionModel
from controllers.user_controller import UserController
from controllers.book_controller import BookController
from controllers.chapter_controller import ChapterController
import urllib.request

# init_db()

user_model = UserModel()
user_cont = UserController()

book_model = BookModel()
book_cont = BookController()

chapter_model = ChapterModel()
chapter_cont = ChapterController()

submissions_model = SubmissionModel()

role_model = RoleModel

chapters = book_cont.get_chapters(1)

students = user_model.get_students()

# user = user_model.get(2)
# pending = submissions_model.teacher_get_pending(user.name)
# for p in pending:
#     print(p.student + "|" + p.b_name + "|" + p.c_name + "|"+p.s_name)


# books = book_model.all()
# for b in books:
#     print(b.name)
# # print(books)

# chapter_cont.add_chapter(1,'asdadad','path')

# print('done')

# res1 = book_cont.add_book('book1')
# print(res1.id)
# res2 = book_cont.add_book('book2')
# print(res2.id)
# user = Users(username="", student_id="2018280142", name="Sam", password="123123", role_id="2")

# a = model.create(user)
# rt;r;,'r

# result = model.get(1)
# print(result.name)
#
# user_id, name, role_id = cont.login("","2018280142","123123")
# print(name)
# print(res.name)

# wiki = "https://en.wikipedia.org/api/rest_v1/page/summary/Eukaryotic_Cells"
# import json
#
# s = ["a", "b", "c"]
# r = json.dumps(s)
# print(r)
from flask_bcrypt import generate_password_hash
hash = generate_password_hash("12345")
print(hash)