from flask import Flask, render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.dream import Dream
from flask_bcrypt import Bcrypt
# from db import mysql
from flask_app.models.comment import Comment


app = Flask(__name__)


app.secret_key = "Kenny."

app.run(debug=True)

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('registration.html')


@app.route('/register', methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/login/page')


@app.route('/login/page')
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email", "login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/login')
    session['user_id'] = user.id
    return redirect('/menu')


@app.route('/menu')
def menu():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("menu.html", user=User.get_by_id(data), dreams=Dream.get_all())


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/new/dream')
def new_dream():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('record.html', user=User.get_by_id(data))


@app.route('/record/dream', methods=['POST'])
def record_dream():
    # print(request.form)
    if 'user_id' not in session:
        return redirect('/logout')
    if not Dream.validate_dream(request.form):
        return redirect('/new/dream')
    data = {
        "dream": request.form["dream"],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "date_of_dream": request.form["date_of_dream"],
        "type_of_dream": request.form["type_of_dream"],
        "user_id": session["user_id"]
    }
    newDream = Dream.save(data)
    id = newDream
    return redirect(f'/dream/{id}')


@app.route('/edit/dream/<int:id>')
def edit_dream(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("edit_dream.html", edit=Dream.get_one(data), user=User.get_by_id(user_data))


@app.route('/update/dream', methods=['POST'])
def update_dream():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Dream.validate_dream(request.form):
        return redirect('/new/dream')
    data = {
        "dream": request.form["dream"],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "date_of_dream": request.form["date_of_dream"],
        "type_of_dream": request.form["type_of_dream"],
        "user_id": session["user_id"]
    }
    Dream.update(data)
    return redirect('/menu')


@app.route('/dream/<int:id>')
def show_dream(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("content.html", dream=Dream.get_one(data), user=User.get_by_id(user_data))


@app.route('/destroy/dream/<int:id>')
def destroy_dream(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Dream.destroy(data)
    return redirect('/menu')


@app.route('/record/comments', methods=['POST'])
def record_comments():
    # print(request.form)
    if 'user_id' not in session:
        return redirect('/logout')
    # if not Dream.validate_dream(request.form):
    #     return redirect('/new/comment')
    userData = {'id': session['user_id']}
    user = User.get_by_id(userData)
    data = {
        "comments": request.form["comments"],
        "first_name": user.first_name,
        "last_name": user.last_name,
        "dreams_id": request.form["dreams_id"],
        "users_id": session["user_id"]
    }
    Comment.save(data)
    id = request.form["dreams_id"]
    return redirect(f'/dreams/{id}/comments')


@app.route('/update/comments', methods=['POST'])
def update_comments():
    if 'user_id' not in session:
        return redirect('/logout')
    # if not Dream.validate_dream(request.form):
    #     return redirect('/new/dream')
    data = {
        "comments": request.form["comments"],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "dreams_id": request.form["dreams_id"],
        "users_id": session["users_id"]
    }
    Comment.update_comments(data)
    return redirect('/new/comments')


@app.route('/new/comments')
def new_comment():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('edit_comment.html', dream=Dream.get_one_with_comments(data), user=User.get_by_id(data))


@app.route('/dreams/<int:id>/comments')
def show_comments(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("edit_comment.html", dream=Dream.get_one_with_comments(data), user=User.get_by_id(user_data))


@app.route('/dreams/destroy/<int:id>/comments')
def destroy_comment(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Comment.destroy_comment(data)
    return redirect('/menu')


@app.route('/edit/comments/<int:id>')
def edit_comments(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("content.html", dream=Dream.get_one_with_comments(data), user=User.get_by_id(user_data))

# @app.route("/")
# def home_view():
#     return render_template("registration.html")


# @app.route("/login/page")
# def login_page():
#     return render_template("login.html")


# @app.route("/")
# def init_view():
#     return index
