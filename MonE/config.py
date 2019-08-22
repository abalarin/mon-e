import os
import json
import urllib3
urllib3.disable_warnings()

with open(os.path.dirname(os.path.abspath(__file__)) + '/config.json') as config_file:
    config = json.load(config_file)


class Config:

    SECRET_KEY = 'a' #os.urandom(12)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    # To suppress FSADeprecationWarning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
