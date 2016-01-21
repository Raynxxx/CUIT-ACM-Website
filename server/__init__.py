from flask import Flask
from flask.ext.login import LoginManager
from config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'

    if not app.debug:
        import logging
        from logging import FileHandler, Formatter

        file_handler = FileHandler(app.config['LOG_DIR'], encoding='utf8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(Formatter(
            '[%(asctime)s] %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(file_handler)

    return app