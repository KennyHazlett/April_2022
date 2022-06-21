import pymysql.cursors
from flask_app import app

class MySQLConnection:
    def __init__(self):

        connection = pymysql.connect(
            host='us-cdbr-east-05.cleardb.net',
            user='b50db7f6268a94',
            password='6653554a',
            db='heroku_3184de52a8125ef',
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
