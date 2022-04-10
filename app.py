import json
import os
from flask import Flask, session
from flask import render_template, flash, request, redirect, url_for, send_from_directory
from engine.graphs import Graphs
from os.path import join, dirname, realpath
from models.user_model import UserModel
from models.book_model import BookModel
from models.submission_model import SubmissionModel
from models.chapter_model import ChapterModel
from models.resource_model import ResourceModel
from controllers.user_controller import UserController
from controllers.book_controller import BookController
from controllers.chapter_controller import ChapterController
from controllers.submission_controller import SubmissionController
from controllers.comment_controller import CommentController
from controllers.response_controller import ResponseController
from controllers.resource_controller import ResourceController
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
RESOURCES_PATH = join(dirname(realpath(__file__)), 'resources\\')
cur_file = ""

# flask
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
app.config['SUBMISSION_FOLDER'] = SUBMISSION_PATH
app.config['RESOURCE_FOLDER'] = RESOURCES_PATH

# # Graph object
g = Graphs()
# Embedding object
# e = Embeddings()

# user model
user_model = UserModel()
book_model = BookModel()
chapter_model = ChapterModel()
submission_model = SubmissionModel()
resource_model = ResourceModel()

user_controller = UserController()
book_controller = BookController()
chapter_controller = ChapterController()
submission_controller = SubmissionController()
comment_controller = CommentController()
response_controller = ResponseController()
resource_controller = ResourceController()


# Base
@app.route('/', methods=['GET', 'POST'])
def index():
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
            student_id = ''
            username = v.strip_tags(username)
            if len(username) == 0 or len(password) == 0:
                return render_template('UI/index.html', auth_message="Invalid login credentials")
        else:  # is student
            student_id = v.strip_tags(student_id)
            if len(student_id) == 0 or len(password) == 0:
                return render_template('UI/index.html', auth_message="Invalid login credentials")

            # user_id, name, role_id\
        res = user_controller.login(username, student_id, password)

        print(res)

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


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# ---------------------------------------------------------------------
# Teacher Routes

@app.route('/teacher/dashboard')
def teacher_dashboard():
    return render_template('UI/teacher/dashboard.html')


@app.route('/teacher/books/add', methods=['GET', 'POST'])
def add_book():
    invalid_files = []

    if request.method == 'GET':
        return render_template('UI/teacher/books/add.html')
    else:
        title = request.form.get('title').strip()
        chapters = request.files.getlist("files[]")

        title = v.strip_tags(title)

        if len(title) == 0:
            return render_template('UI/teacher/add.html', message='Please provide a title')

        if len(chapters) == 0:
            return render_template('UI/teacher/add.html', message='Please upload chapters')

        # create folders
        title = title.capitalize()
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


@app.route('/teacher/view_student_submission/<sname>')
def view_student_graph(sname):
    data_path = SUBMISSION_PATH + "json\\" + sname + ".json"

    if request.accept_mimetypes.best == "application/json":
        json_data = g.display_graph(data_path, "dd", False)
        # print(json_data)
        return str(json_data)

    return render_template("UI/teacher/submissions/student_graph.html", data=sname)


@app.route('/teacher/submissions')
def view_submissions():
    user = user_model.get(int(session.get('user_id')))
    submissions = submission_model.teacher_get_pending(str(user.name))
    return render_template('UI/teacher/submissions/view_submissions.html', data=submissions)


@app.route('/teacher/check_similarity/<book>/<chapter>/<sub_name>')
def check_similarity(book, chapter, sub_name):
    submission = submission_model.get_by_name(sub_name)
    user = user_model.get(submission.student_id)
    student = user.name
    return render_template('UI/teacher/submissions/similarity.html', book=book, chapter=chapter, sub=sub_name,
                           student=student)


@app.route('/do_similarity/<book>/<chapter>/<sub_name>')
def do_similarity(book, chapter, sub_name):
    wiki_data = []
    vv = []
    doc1 = g.get_book_content(JSON_PATH + book.capitalize() + "/" + chapter + ".json")
    doc2 = g.get_book_content(SUBMISSION_PATH + "json\\" + sub_name + ".json")
    topics = doc1.split("\n")

    for t in topics[0:len(topics) - 1]:
        t = t.strip()
        t = t.replace(" ", "_")
        wiki_data.append(t)
    wiki_data.append(doc2)

    if request.accept_mimetypes.best == "application/json":
        return json.dumps(wiki_data)
    return ''


@app.route('/teacher_update_submissions/<sub_name>')
def update_submission(sub_name):
    if request.accept_mimetypes.best == "application/json":
        score = request.args['score']
        status = "checked"

        submission_model.update(sub_name, status, score)

        print(score)
    return ''


# ---------------------------------------------------------------------
# Student Route

@app.route('/student/books')
def student_view_books():
    books = book_model.all()
    user = user_model.get(session.get('user_id'))
    return render_template('UI/student/books/view_books.html', data=books, user=user)


@app.route('/student/book/similarity/<book_id>')
def view_cummulative_similarity(book_id):
    user_id = session.get('user_id')
    book = book_model.get(book_id)
    chapters = chapter_model.get_all_chapters_by_book_id(book_id)
    submissions = submission_model.get_student_submissions_by_book(user_id, book_id)

    book_chapters = {}
    total_score = 0

    for c in chapters:
        book_chapters[c.name] = float(0)

    for s in submissions:
        if s.cname in book_chapters:
            book_chapters[s.cname] = s.score

    for k, v in book_chapters.items():
        total_score += float(v)

    total_score = total_score / len(book_chapters)

    return render_template('UI/student/books/cumulative.html', data=book_chapters,
                           book=book.name,
                           score=str(total_score) + "%")


@app.route('/student/posts/add', methods=['GET', 'POST'])
def add_post():
    if request.method == "POST":
        chapter_id = request.form.get("chapter_id")
        comment = request.form.get("post").strip()
        comment = v.strip_tags(comment)

        if len(comment) == 0:
            return render_template('UI/student/comments/add.html', message="A post cannot be empty")

        user_id = session.get('user_id')
        res = comment_controller.add_comment(user_id, chapter_id, comment)

        chapter_data = chapter_model.get(chapter_id)
        book = book_model.get(chapter_data.book_id)
        posts = comment_controller.get_chapter_posts(chapter_id)

        data_path = JSON_PATH + book.name + "/" + chapter_data.name + ".json"

        if request.accept_mimetypes.best == "application/json":
            json_data = g.display_graph(data_path, "dd", False)
            return str(json_data)

        return render_template('UI/student/graph.html',
                               chapter_id=chapter_data.id,
                               chapter=chapter_data.name.capitalize(),
                               book_id=chapter_data.book_id,
                               posts=posts)

        # if not res:
        #     return render_template('UI/student/comments/add.html', message="Something happened. Try again later!")
        # else:
        #     return redirect(url_for('view_posts'))

    return render_template('UI/student/comments/add.html')


@app.route('/student/book/chapter/graph/<chapter>/<id>', methods=['GET', 'POST'])
def student_view_graph(chapter, id):
    chapter_data = chapter_model.get(id)
    book = book_model.get(chapter_data.book_id)
    posts = comment_controller.get_chapter_posts(id)

    data_path = JSON_PATH + book.name + "/" + chapter + ".json"

    if request.accept_mimetypes.best == "application/json":
        json_data = g.display_graph(data_path, "dd", False)
        return str(json_data)

    # if request.method == 'POST':
    #     chapter_id = request.form.get("chapter_id")
    #     comment = request.form.get("post").strip()
    #     comment = v.strip_tags(comment)
    #
    #     if len(comment) == 0:
    #         return render_template('UI/student/comments/add.html', message="A post cannot be empty")
    #
    #     user_id = session.get('user_id')
    #     res = comment_controller.add_comment(user_id, chapter_id, comment)
    #
    #     if not res:
    #         return render_template('UI/student/comments/add.html', message="Something happened. Try again later!")
    #     else:
    #         return redirect(url_for('view_posts'))

    return render_template('UI/student/graph.html',
                           chapter_id=chapter_data.id,
                           chapter=chapter.capitalize(),
                           book_id=chapter_data.book_id,
                           posts=posts)


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


@app.route('/student/posts')
def view_posts():
    posts = comment_controller.get_posts()
    return render_template('UI/student/comments/view_posts.html', data=posts)


@app.route('/student/posts/<id>')
def view_post(id):
    post = comment_controller.get_post(id)
    user = user_model.get(post.user_id)

    responses = response_controller.get_responses(id)
    return render_template('UI/student/responses/add_response.html', post=post, user=user, responses=responses)


#
#
# @app.route('/student/posts/my')
# def view_my_post():
#     posts = comment_controller.get_user_posts(session.get('user_id'))
#     return render_template('UI/student/comments/my_posts.html', data=posts)


@app.route('/student/response/post/<id>/add', methods=['POST'])
def add_response(id):
    reply = request.form.get("reply").strip()
    reply = v.strip_tags(reply)
    user_id = session.get('user_id')

    response_controller.add_response(id, user_id, reply)

    return redirect(url_for('view_post', id=id))


@app.route('/student/resource/view_resources')
def view_resources():
    resources = resource_controller.get_resources()
    return render_template('UI/student/resources/view_resources.html', data=resources)


@app.route('/student/resource/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist("files[]")
        desc = request.form.get("description").strip()
        desc = v.strip_tags(desc)

        if len(desc) == 0 or len(files) == 0:
            return render_template('UI/student/resources/upload.html', message="Error uploading resource")

        for f in files:
            user_id = session.get('user_id')
            ext = f.filename.split(".")[1].lower()
            name = f.filename.split(".")[0].lower()
            resource_id = uuid.uuid4().hex
            f.filename = resource_id + "." + ext

            f.save(app.config['RESOURCE_FOLDER'] + "//" + f.filename.lower())
            resource_controller.upload(user_id, name, resource_id + "." + ext, desc)

            return render_template('UI/student/resources/upload.html', success='Resource added')

    return render_template('UI/student/resources/upload.html')


@app.route('/student/resource/download/<rid>')
def download(rid):
    resource = resource_model.get(rid)
    num_downloads = resource.downloads + 1
    resource_controller.update_downloads(rid, num_downloads)

    return send_from_directory(app.config['RESOURCE_FOLDER'], rid)


# ---------------------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True, port=5000)
