from dataclasses import dataclass, field
from typing import Optional
from os import environ
from os.path import dirname, split, join
from typing import Literal


root_dir = dirname(__file__)
app_dir = join(root_dir, 'app')

@dataclass(init=False)
class Config:
    SECRET_KEY: str = 'bite my shiny metal ass'
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///'+join(root_dir, 'tempdb.sqlite')
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
                val = environ.get(k, default)

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
