from flask import Flask
from flask import render_template, redirect, session, request, flash

app = Flask(__name__)


app.secret_key = "Kenny."


@app.route("/")
def home_view():
    return render_template("registration.html")


@app.route("/login/page")
def login_page():
    return render_template("login.html")


# @app.route("/")
# def init_view():
#     return index
