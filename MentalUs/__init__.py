# encoding=utf-8
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from helpers import customize_login_manager
import logging


db = SQLAlchemy()
login_manager = LoginManager()
customize_login_manager(login_manager)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    # register_blueprints
    from user import user
    from general import general
    from scale import scale
    app.register_blueprint(general)
    app.register_blueprint(user)
    app.register_blueprint(scale)

    return app