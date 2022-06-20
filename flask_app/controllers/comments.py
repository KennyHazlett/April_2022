from flask import render_template, redirect, session, request
from __init__ import app
from flask_app.models.dream import Dream
from flask_app.models.user import User
from flask_app.models.comment import Comment


@app.route('/record/comments', methods=['POST'])
def record_comments():
    # print(request.form)
    if 'user_id' not in session:
        return redirect('/logout')
    # if not Dream.validate_dream(request.form):
    #     return redirect('/new/comment')
    userData = {'id': session['user_id']}
    user = User.get_by_id(userData)
    data = {
        "comments": request.form["comments"],
        "first_name": user.first_name,
        "last_name": user.last_name,
        "dreams_id": request.form["dreams_id"],
        "users_id": session["user_id"]
    }
    Comment.save(data)
    id = request.form["dreams_id"]
    return redirect(f'/dreams/{id}/comments')


@app.route('/update/comments', methods=['POST'])
def update_comments():
    if 'user_id' not in session:
        return redirect('/logout')
    # if not Dream.validate_dream(request.form):
    #     return redirect('/new/dream')
    data = {
        "comments": request.form["comments"],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "dreams_id": request.form["dreams_id"],
        "users_id": session["users_id"]
    }
    Comment.update_comments(data)
    return redirect('/new/comments')


@app.route('/new/comments')
def new_comment():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('edit_comment.html', dream=Dream.get_one_with_comments(data), user=User.get_by_id(data))


@app.route('/dreams/<int:id>/comments')
def show_comments(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("edit_comment.html", dream=Dream.get_one_with_comments(data), user=User.get_by_id(user_data))


@app.route('/dreams/destroy/<int:id>/comments')
def destroy_comment(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Comment.destroy_comment(data)
    return redirect('/menu')


@app.route('/edit/comments/<int:id>')
def edit_comments(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("content.html", dream=Dream.get_one_with_comments(data), user=User.get_by_id(user_data))
