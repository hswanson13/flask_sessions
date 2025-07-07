from flask import Flask
from config import the_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_sqlakeyset import KeySetPagination
app = Flask(__name__)
app.config.from_object(the_config) #tells flask to read config file

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flask_login import LoginManager
login = LoginManager(app)
login.login_view = 'login'

from app import routes, forms