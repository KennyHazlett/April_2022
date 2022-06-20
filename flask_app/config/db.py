from flask_app import app
from flaskext.mysql import MySQL
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'b50db7f6268a94'
app.config['MYSQL_DATABASE_PASSWORD'] = '6653554a'
app.config['MYSQL_DATABASE_DB'] = 'heroku_3184de52a8125ef'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-05.cleardb.net'
mysql.init_app(app)
