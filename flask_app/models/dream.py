from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.comment import Comment


class Dream:
    db_name = 'dream_schema'

    def __init__(self, db_data):
        self.id = db_data['id']
        self.dream = db_data['dream']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.date_of_dream = db_data['date_of_dream']
        self.type_of_dream = db_data['type_of_dream']
        self.comments = []
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO dreams (dream, first_name, last_name, date_of_dream, type_of_dream, user_id) VALUES (%(dream)s,%(first_name)s,%(last_name)s,%(date_of_dream)s,%(type_of_dream)s,%(user_id)s);"
        return connectToMySQL().query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dreams;"
        results = connectToMySQL().query_db(query)
        all_dreams = []
        for row in results:
            print(row['date_of_dream'])
            all_dreams.append(cls(row))
        return all_dreams

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM dreams WHERE id = %(id)s;"
        results = connectToMySQL().query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_one_with_comments(cls, data):
        query = "SELECT * FROM dreams LEFT JOIN comments on dreams.id = comments.dreams_id WHERE dreams.id = %(id)s;"
        results = connectToMySQL().query_db(query, data)
        # print(results)
        dream = cls(results[0])
        for data in results:
            x = {
                'id': data['comments.id'],
                'first_name': data['comments.first_name'],
                'last_name': data['comments.last_name'],
                'comments': data['comments'],
                'dreams_id': data['dreams_id'],
                'users_id': data['users_id'],
                'created_at': data['created_at'],
                'updated_at': data['updated_at']
            }
            dream.comments.append(Comment(x))
        return dream
        # return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE dreams SET dream=%(dream)s, first_name=%(first_name)s, last_name=%(last_name)s, date_of_dream=%(date_of_dream)s, type_of_dream=%(type_of_dream)s, created_at= NOW() updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL().query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM dreams WHERE id = %(id)s;"
        return connectToMySQL().query_db(query, data)

    @staticmethod
    def validate_dream(dream):
        is_valid = True
        if len(dream['dream']) < 10:
            is_valid = False
            flash("You Must Describe Your Dream With At Least 10 Characters", "dream")
        if len(dream['first_name']) < 2:
            is_valid = False
            flash("First Name Must Be At Least 2 Characters", "dream")
        if len(dream['last_name']) < 2:
            is_valid = False
            flash("Last Name Must Be At Least 2 Characters", "dream")
        if dream['date_of_dream'] == "":
            is_valid = False
            flash("You Must Select A Date", "dream")
        if len(dream['type_of_dream']) < 1:
            is_valid = False
            flash("You Must Select A Type Of Dream", "dream")
        return is_valid
