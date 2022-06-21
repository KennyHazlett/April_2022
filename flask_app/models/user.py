from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db = "dream_schema"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL().query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL().query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL().query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL().query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:
            flash("Email Already Taken. Use Another!", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Wrong Email Address! Try Again!", "register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First Name Must Be At Least 2 Characters", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name Must Be At Least 2 Characters", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password Must Be At Least 8 Characters AND Should Be One You Have Never Used Before!", "register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords Do Not Match, Try Again!", "register")
            is_valid = False
        if not any(char.isdigit() for char in user['password']):
            flash('Password Should Have At Least One Number', "register")
            print('Password Should Have At Least One Numberr')
            is_valid = False
        if not any(char.isupper() for char in user['password']):
            flash('Password Should Have At Least One Uppercase Letter', "register")
            print('Password Should Have At Least One Uppercase Letter')
            is_valid = False
        return is_valid
