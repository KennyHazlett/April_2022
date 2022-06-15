from flask import Flask

app = Flask(__name__)

app.secret_key = "Kenny."


@app.route("/")
def home_view():
    return "./templates/registration.html"
