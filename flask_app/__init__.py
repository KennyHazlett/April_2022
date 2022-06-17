from flask import Flask
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.dream import Dream
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = "Kenny."


@app.route("/")
def home_view():
    return render_template("registration.html")


@app.route("/login/page")
def login_page():
    return render_template("login.html")


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
# @app.route("/")
# def init_view():
#     return index
