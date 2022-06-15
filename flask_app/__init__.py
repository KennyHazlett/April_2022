from flask import Flask, render_template

app = Flask(__name__)

app.secret_key = "Kenny."


@app.route("/")
def index():
    return render_template("registration.html")
