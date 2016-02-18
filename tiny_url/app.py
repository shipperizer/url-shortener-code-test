from logging import StreamHandler
from flask.ext.migrate import Migrate
from flask import Flask
import os

from tiny_url.db import db
from tiny_url.exceptions import ResourceNotFound, RequestError, ResourceExists
from tiny_url.blueprints.api import api


def init_config(app):
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASS = os.environ.get('DB_PASS', 'postgres')
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_PORT = os.environ.get('DB_PORT', 5432)
    DB_NAME = os.environ.get('DB_NAME', 'tiny_url')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'lol')
    DEBUG = os.environ.get('DEBUG') is not None
    app.config['DEBUG'] = DEBUG
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%s:%s@%s:%s/%s' % (
        DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
    )
    app.secret_key = SECRET_KEY
    app.logger.addHandler(StreamHandler())


def create_app():
    app = Flask(__name__)
    init_config(app)
    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(api)

    @app.errorhandler(ResourceNotFound)
    @app.errorhandler(RequestError)
    @app.errorhandler(ResourceExists)
    def handle_invalid_usage(error):
        return error.message, error.status_code

    return app
