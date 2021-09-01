from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pymysql

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://b2cdbfe6672f14:01921dc8@us-cdbr-east-04.cleardb.com/heroku_39c807b6bb86bdc?reconnect=true"
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.config.from_object(Config)

from app import routes