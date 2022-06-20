from flask import Flask, render_template
from flask_app import controllers


app = Flask(__name__)


app.secret_key = "Kenny."

app.run(debug=True)


# @app.route("/")
# def home_view():
#     return render_template("registration.html")


# @app.route("/login/page")
# def login_page():
#     return render_template("login.html")


# @app.route("/")
# def init_view():
#     return index
