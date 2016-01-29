from flask import Flask
from config import config
from flask.ext.migrate import Migrate
from flask.ext.login import LoginManager
from .model import db


app = Flask(__name__)
migrate = Migrate()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'api.login'


def create_app(config_name):
    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    if not app.debug:
        import logging
        from logging import FileHandler, Formatter

        file_handler = FileHandler(app.config['LOG_DIR'], encoding='utf8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(Formatter(
            '[%(asctime)s] %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(file_handler)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    from .view import view as view_blueprint
    app.register_blueprint(view_blueprint)

    return app