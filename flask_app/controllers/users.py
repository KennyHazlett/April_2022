from flask import render_template, redirect, session, request, flash
from flask_app.__init__ import app
from flask_app.models.user import User
from flask_app.models.dream import Dream
from flask_bcrypt import Bcrypt
from db import mysql
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
