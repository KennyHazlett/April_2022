from flask import Flask
from flask import render_template
from flask_app.controllers import comments, dreams, users
from flask_app.models import comment, dream, user
from flask_app.templates import content, edit_content, edit_dream, login, menu, record, registration


app = Flask(__name__)


app.secret_key = "Kenny."


# @app.route("/")
# def home_view():
#     return render_template("registration.html")


# @app.route("/login/page")
# def login_page():
#     return render_template("login.html")


# @app.route("/")
# def init_view():
#     return index
