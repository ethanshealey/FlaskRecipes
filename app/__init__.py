from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pymysql

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:pass@127.0.0.1/recipes"
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.config.from_object(Config)

from app import routes