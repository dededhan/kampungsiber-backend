from app import app
from flaskext.mysql import MySQL
from flask_cors import CORS
from datetime import timedelta, datetime

app.config['SECRET_KEY'] = 'kampungsiber-key-dev'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=20)
CORS(app)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'dev-kampungsiber-db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)