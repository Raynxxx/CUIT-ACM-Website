import os
from datetime import timedelta


basedir = os.path.split(os.path.realpath(__file__))[0]


class Config:
    SSL_DISABLE = True
    CSRF_ENABLED = True
    SECRET_KEY = 'a hard guess string'

    # database
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # session, cookie
    PERMANENT_SESSION_LIFETIME = timedelta(days=3)
    REMEMBER_COOKIE_DURATION = timedelta(days=3)

    # upload file
    UPLOADED_RESOURCE_DEST = basedir + '/uploads/'

    # log
    LOG_DIR = basedir + '/log/error.log'


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:63005610@localhost/cuit_acm?useUnicode=true&characterEncoding=utf-8'


class DeployConfig(Config):
    SECRET_KEY = 'gefdger3fs'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:ogre@localhost/cuit_acm?useUnicode=true&characterEncoding=utf-8'


config = {
    'dev': DevConfig,
    'deploy': DeployConfig,

    'default': DevConfig
}