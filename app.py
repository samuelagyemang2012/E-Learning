import json
import os
from flask import Flask, session
from flask import render_template, flash, request, redirect, url_for
from engine.graphs import Graphs
from os.path import join, dirname, realpath
from models.user_model import UserModel
from models.book_model import BookModel
from models.submission_model import SubmissionModel
from models.chapter_model import ChapterModel
from controllers.user_controller import UserController
from controllers.book_controller import BookController
from controllers.chapter_controller import ChapterController
from controllers.submission_controller import SubmissionController
from datetime import date
import uuid
import validation.validation as v

# from engine.embeddings import Embeddings
# from models import book_migration, user_migration, chapter_migration, roles_migration
# from routes import role_routes
import config
import re

JSON_PATH = join(dirname(realpath(__file__)), "books\\json\\")
UPLOADS_PATH = join(dirname(realpath(__file__)), 'books\\xml\\')
SUBMISSION_PATH = join(dirname(realpath(__file__)), 'submissions\\')
cur_file = ""

# flask
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
app.config['SUBMISSION_FOLDER'] = SUBMISSION_PATH

# # Graph object
g = Graphs()
# Embedding object
# e = Embeddings()

# user model
user_model = UserModel()
book_model = BookModel()
chapter_model = ChapterModel()
submission_model = SubmissionModel()

user_controller = UserController()
book_controller = BookController()
chapter_controller = ChapterController()
submission_controller = SubmissionController()


# Base
@app.route('/', methods=['GET', 'POST'])
def index():
    strip_tags = re.compile('<.*?>')

    if request.method == 'GET':
        return render_template('UI/index.html')
    else:
        # Strip whitespace
        is_teacher = request.form.get("is_teacher")
        password = request.form.get('password')
        username = request.form.get("username").strip()
        student_id = request.form.get("student_id").strip()

        # is teacher
        if is_teacher == 'on':
            username = re.sub(strip_tags, "", username)
            if len(username) == 0 or len(password) == 0:
                return render_template('UI/index.html', auth_message="Invalid login credentials")
        else:  # is student
            student_id = re.sub(strip_tags, "", student_id)
            if len(student_id) == 0 or len(password) == 0:
                return render_template('UI/index.html', auth_message="Invalid login credentials")

            # user_id, name, role_id\
        res = user_controller.login(username, student_id, password)

        if not res:
            return render_template('UI/index.html', auth_message="Invalid login credentials")
        else:
            user_id = res[0]
            role_id = res[1]
            session['user_id'] = user_id
            ID = user_id
            # teacher
            if role_id == 1:
                return redirect(url_for('teacher_dashboard'))
            else:  # student
                return redirect(url_for('student_view_books'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('UI/register.html')
    else:
        username = request.form.get("username").strip()
        student_id = request.form.get("student_id").strip()
        firstname = request.form.get("firstname").strip()
        lastname = request.form.get("lastname").strip()
        # email = request.form.get("email").strip()
        password = request.form.get("password").strip()
        confirm_password = request.form.get("c_password")
        is_teacher = request.form.get("is_teacher")

        if is_teacher == 'on':
            if (len(username) == 0 or len(firstname) == 0 or len(lastname) == 0 or len(
                    password) == 0 or len(confirm_password) == 0):
                flash("Please fill in the required information")
                return redirect('/register')

            if not v.validate_string(username, 6) or not v.validate_string(firstname, 2) or not v.validate_string(
                    lastname, 2) or not v.validate_string(password, 8) or not v.compare_passwords(password,
                                                                                                  confirm_password):
                flash('Please verify your information')
                return redirect('/register')

            res = user_controller.register(username, "", password, firstname + " " + lastname, 1)
            if res:
                flash("Registration successful")
                return redirect('/')
            else:
                flash("Something went wrong")
                return redirect('/register')
        else:
            if (len(student_id) == 0 or len(firstname) == 0 or len(lastname) == 0 or len(
                    password) == 0 or len(confirm_password) == 0):
                flash("Please fill in the required information")
                return redirect('/register')

            if not v.validate_string(student_id, 10) or not v.validate_string(firstname, 2) or not v.validate_string(
                    lastname, 2) or not v.validate_string(password, 8) or not v.compare_passwords(password,
                                                                                                  confirm_password):
                flash('Please verify your information')
                return redirect('/register')

            res = user_controller.register("", student_id, password, firstname + " " + lastname, 2)
            if res:
                flash("Registration successful")
                return redirect('/')
            else:
                flash("Something went wrong")
                return redirect('/register')

    # return render_template('UI/register.html')


# ---------------------------------------------------------------------
# Teacher Routes

@app.route('/teacher/dashboard')
def teacher_dashboard():
    return render_template('UI/teacher/dashboard.html')


@app.route('/teacher/books/add', methods=['GET', 'POST'])
def add_book():
    invalid_files = []
    strip_tags = re.compile('<.*?>')

    if request.method == 'GET':
        return render_template('UI/teacher/books/add.html')
    else:
        title = request.form.get('title').strip()
        chapters = request.files.getlist("files[]")

        title = re.sub(strip_tags, "", title)

        if len(title) == 0:
            return render_template('UI/teacher/add.html', message='Please provide a title')

        if len(chapters) == 0:
            return render_template('UI/teacher/add.html', message='Please upload chapters')

        # create folders
        os.mkdir(app.config['UPLOAD_FOLDER'] + title)
        os.mkdir(JSON_PATH + title)

        book_id = book_controller.add_book(title)

        for ch in chapters:
            ext = ch.filename.split(".")[1].lower()
            ch_name = ch.filename.split(".")[0].lower()
            ch_path = app.config['UPLOAD_FOLDER'] + title + "//" + ch.filename.lower()

            if ext != 'xml':
                invalid_files.append(ch.filename)
            else:
                ch.save(app.config['UPLOAD_FOLDER'] + title + "//" + ch.filename.lower())
                g.parse_xml(UPLOADS_PATH + title + "//" + ch.filename,
                            JSON_PATH + title + "//" + ch.filename.split(".")[0] + ".json")

                chapter_controller.add_chapter(book_id, ch_name, ch_path)
        return render_template('UI/teacher/books/add.html', success='Book added')


@app.route('/teacher/books')
def view_books():
    books = book_model.all()
    return render_template('UI/teacher/books/view_books.html', data=books)


@app.route('/teacher/book/chapters/<id>')
def view_chapter(id):
    chapters = book_controller.get_chapters(id)
    return render_template('UI/teacher/books/chapters.html', data=chapters)


@app.route('/teacher/book/chapter/graph/<chapter>/<id>')
def view_graph(chapter, id):
    chapter_data = chapter_model.get(id)
    book = book_model.get(chapter_data.book_id)

    data_path = JSON_PATH + book.name + "/" + chapter + ".json"

    if request.accept_mimetypes.best == "application/json":
        json_data = g.display_graph(data_path, "dd", False)
        return str(json_data)

    return render_template('UI/teacher/graph.html', chapter=chapter.capitalize(), book_id=chapter_data.book_id)


@app.route('/teacher/submissions')
def view_submissions():
    user = user_model.get(int(session.get('user_id')))
    submissions = submission_model.teacher_get_pending(str(user.name))
    return render_template('UI/teacher/submissions/view_submissions.html', data=submissions)


@app.route('/teacher/submissions/check_similarity/<id>')
def check_similarity(id):
    submission = submission_model.get(id)
    student = user_model.get(submission.student_id)
    book = book_model.get(submission.book_id)
    chapter = chapter_model.get(submission.chapter_id)

    teacher_file_path = JSON_PATH + book.name + "/" + chapter.name + ".json"
    student_file_path = SUBMISSION_PATH + submission.name + ".json"

    if request.accept_mimetypes.best == "application/json":
        teacher_data = g.display_graph(teacher_file_path, "dd", False)
        student_data = g.display_graph(student_file_path, "dd", False)

        return {"teacher_data": teacher_data, "student_data": student_data}

    return render_template('UI/teacher/submissions/check_similarity.html')


# ---------------------------------------------------------------------
# Student Route

@app.route('/student/books')
def student_view_books():
    books = book_model.all()
    return render_template('UI/student/books/view_books.html', data=books)


@app.route('/student/book/chapter/graph/<chapter>/<id>')
def student_view_graph(chapter, id):
    chapter_data = chapter_model.get(id)
    book = book_model.get(chapter_data.book_id)

    data_path = JSON_PATH + book.name + "/" + chapter + ".json"

    if request.accept_mimetypes.best == "application/json":
        json_data = g.display_graph(data_path, "dd", False)
        return str(json_data)

    return render_template('UI/student/graph.html', chapter=chapter.capitalize(), book_id=chapter_data.book_id)


@app.route('/student/book/chapters/<id>')
def student_view_chapter(id):
    chapters = book_controller.get_chapters(id)
    return render_template('UI/student/books/chapters.html', data=chapters)


@app.route('/student/add_submission', methods=['GET', 'POST'])
def add_submission():
    if request.method == 'GET':
        books = book_model.all()
        teachers = user_model.get_teachers()

        if request.accept_mimetypes.best == "application/json":
            data = []
            book_id = request.args['chapter_id']
            chapters = book_controller.get_chapters(book_id)

            for c in chapters:
                d = {"id": c.id, "name": c.name}
                data.append(d)

            return json.dumps(data)

        return render_template('UI/student/submissions/add.html', books=books, teachers=teachers)

    else:
        teacher_id = request.form.get("teacher_id").strip()
        books_id = request.form.get("books_id").strip()
        chapter_id = request.form.get("chapter_id").strip()
        student_id = session.get('user_id')
        student = user_model.get(student_id)

        if 'file' not in request.files:
            flash('No file found')
            return redirect(request.url)

        submission_file = request.files['file']

        file_split = submission_file.filename.split(".")

        if file_split[1] != "xml":
            flash("Invalid file type. Only .xml file allowed")
            return redirect(request.url)

        name = student.student_id + "-" + file_split[0] + "-" + uuid.uuid4().hex
        submission_file.filename = name + ".xml"

        submission_file.save(app.config['SUBMISSION_FOLDER'] + "xml/" + submission_file.filename)
        g.parse_xml(SUBMISSION_PATH + "xml/" + submission_file.filename,
                    SUBMISSION_PATH + "json/" + name + ".json")
        print(submission_file.filename)

        submission_controller.add(student_id, teacher_id, books_id, chapter_id, name, "pending", "-")
        flash('Submitted successfully')
        return redirect(request.url)
        # return render_template('UI/student/submissions/add.html', success='Submitted successfully')


@app.route('/student/submissions/pending')
def get_pending_submissions():
    pending = submission_model.student_get_pending(session.get('user_id'))
    return render_template('UI/student/submissions/pending.html', data=pending)


@app.route('/student/submissions/checked')
def get_checked_submissions():
    checked = submission_model.student_get_checked(session.get('user_id'))
    return render_template('UI/student/submissions/checked.html', data=checked)


# ---------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
