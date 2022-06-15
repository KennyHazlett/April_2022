from flask import Flask, render_template
from .controllers.users import index

app = Flask(__name__)

app.secret_key = "Kenny."


@app.route("/")
def home_view():
    return "./templates/registration.html"


# @app.route("/")
# def init_view():
#     return index
