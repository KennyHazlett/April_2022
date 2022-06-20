from flask import render_template, redirect, session, request
from __init__ import app
from flask_app.models.dream import Dream
from flask_app.models.user import User


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
