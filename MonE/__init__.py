from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

from MonE.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    # Init app contenxts
    db.init_app(app)
    ma.init_app(app)

    # Init Login LoginManager
    from MonE.models.users import load_user
    login_manager.init_app(app)
    login_manager.user_loader(load_user)

    from MonE.endpoints.main.routes import main
    from MonE.endpoints.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
