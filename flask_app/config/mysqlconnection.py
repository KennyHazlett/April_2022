import pymysql.cursors
from flask_app import app

class MySQLConnection:
    def __init__(self):

        connection = pymysql.connect(
            host=app.config['MYSQL_DATABASE_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_DATABASE_PASSWORD'],
            db=app.config['MYSQL_DATABASE_DB'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True)

        self.connection = connection

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:

                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:

                    result = cursor.fetchall()
                    return result
                else:

                    self.connection.commit()
            except Exception as e:

                print("Something went wrong", e)
                return False
            finally:

                self.connection.close()


def connectToMySQL():
    return MySQLConnection()
