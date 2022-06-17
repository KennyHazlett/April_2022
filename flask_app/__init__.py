from flask import Flask, render_template
app = Flask(__name__)

app.secret_key = "Kenny."


@app.route("/")
def home_view():
    return render_template("registration.html")


# @app.route("/")
# def init_view():
#     return index
