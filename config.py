from dataclasses import dataclass, field
import os
from typing import Literal

basedir = os.path.abspath(os.path.dirname(__file__))
app_dir = os.path.join(basedir, 'app')

@dataclass(init=False)
class Config:
    SECRET_KEY: str = 'bite my shiny metal ass'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    FLASK_APP="microblog.py"
    
    @property
    def keys(self):
        #get all keys from this config, do uppercase ones which are the environment variable keys
        keys = []
        for k in dir(self):
            if k[0].isupper():
                keys.append(k)
        return keys

    def __init__(self):
        for k in self.keys:
            #looks for environment variables in:
            #1. env.py, defined personal secrets in env.py file
            #2. environement, defined in the environement it is ran in here
            #3. here, the default, defined here in Config class
            default = getattr(self, k)
            try:
                import env_personal
                val = getattr(env_personal, k)
            except (ImportError, AttributeError):
                val = os.environ.get(k, default)

            if type(default) == bool:
                if str(val).lower() == "true":
                    val = True
                elif str(val).lower() == "false":
                    val = False
                else:
                    raise ValueError(f"Boolean config \"{k}\" must be True or False, found \"{val}\"")

            else:
                val = type(default)(val)

            setattr(self, k, val)


the_config = Config()

# in another file
# from config import the_config
