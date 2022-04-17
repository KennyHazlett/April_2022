from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Comment:
    db_name = 'dream_schema'

    def __init__(self, data):
        self.id = data['id']
        self.comments = data['comments']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.dreams_id = data['dreams_id']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO comments (comments, first_name, last_name, dreams_id, users_id, created_at, updated_at) VALUES (%(comments)s, %(first_name)s, %(last_name)s, %(dreams_id)s, %(users_id)s, NOW(), NOW());"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def destroy_comment(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
