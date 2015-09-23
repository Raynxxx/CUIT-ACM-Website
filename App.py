# coding=utf-8
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.uploads import configure_uploads, patch_request_class
from server.resource_server import resource
from dao.db import db
from dao.dbBase import  User
from view.admin import admin
from view.profile import profile
from view.ajax import ajax
from view.index import main

app = Flask(__name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


def init():
    app.config.from_pyfile('config.py')
    db.init_app(app)
    import logging
    from logging import FileHandler
    from logging import Formatter

    file_handler = FileHandler(app.root_path + "/log/web_errors.log")
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(profile)
    app.register_blueprint(ajax)
    patch_request_class(app, size=16*1024*1024)
    configure_uploads(app, resource)


if __name__ == '__main__':
    init()
    app.run(debug=True)