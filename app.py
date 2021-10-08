import os

import wikipediaapi
from flask import Flask, session
from flask import render_template, flash, request, redirect, url_for
from engine.graphs import Graphs
from os.path import join, dirname, realpath
from models.user_model import UserModel
from models.book_model import BookModel
from models.chapter_model import ChapterModel
from controllers.user_controller import UserController
from controllers.book_controller import BookController
from controllers.chapter_controller import ChapterController
import validation.validation as v
# from engine.embeddings import Embeddings
# from models import book_migration, user_migration, chapter_migration, roles_migration
# from routes import role_routes
import wikipediaapi
import config
import re

json_path = join(dirname(realpath(__file__)), "books\\json\\")
UPLOADS_PATH = join(dirname(realpath(__file__)), 'books\\xml\\')
cur_file = ""

# flask
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

# # Graph object
g = Graphs()
# Embedding object
# e = Embeddings()
# Wikipedia object
wiki = wikipediaapi.Wikipedia('en')

# user model
user_model = UserModel()
book_model = BookModel()
chapter_model = ChapterModel()

user_controller = UserController()
book_controller = BookController()
chapter_controller = ChapterController()


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
            # teacher
            if role_id == 1:
                return redirect(url_for('teacher_dashboard'))
            else:  # student
                return "student"


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
        os.mkdir(json_path + title)

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
                            json_path + title + "//" + ch.filename.split(".")[0] + ".json")

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

    data_path = json_path + book.name + "/" + chapter + ".json"

    if request.accept_mimetypes.best == "application/json":
        json_data = g.display_graph(data_path, "dd", False)
        return str(json_data)

    return render_template('UI/teacher/graph.html', data=chapter.capitalize())


@app.route('/teacher/students')
def view_students():
    students = user_model.get_students()
    return render_template('UI/teacher/students/view_students.html', data=students)

# ---------------------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True, port=5000)
