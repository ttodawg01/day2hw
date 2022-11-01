from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
# add a SECRET_KEY to the app config

# app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config.from_object(Config)

db = SQLAlchemy(app)
#create an instance of loginmanager to let our app have login capability
login = LoginManager(app)
login.login_view = 'login'

migrate = Migrate(app, db, render_as_batch = True)

from . import routes, models