from flask import Flask
from config import the_config

app = Flask(__name__)
app.config.from_object(the_config) #tells flask to read config file

from app import routes