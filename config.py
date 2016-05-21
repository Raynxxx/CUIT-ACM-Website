import os
from datetime import timedelta


basedir = os.path.split(os.path.realpath(__file__))[0]


class Config:
    SSL_DISABLE = True
    CSRF_ENABLED = True
    SECRET_KEY = 'a hard guess string'
    EncryptionKey = 'Y3VpdGFj'
    IV = '\x22\x33\x35\x81\xBC\x38\x5A\xE7'

    # database
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DB_URI_TEMPLATE = 'mysql://root:{}@localhost/cuit_acm'

    # session, cookie
    PERMANENT_SESSION_LIFETIME = timedelta(days=3)
    REMEMBER_COOKIE_DURATION = timedelta(days=3)

    # upload file
    UPLOADED_RESOURCE_DEST = basedir + '/uploads/'

    # log
    LOG_DIR = basedir + '/log/error.log'


class DevConfig(Config):
    DEBUG = True
    PASSWORD = '63005610'
    SQLALCHEMY_DATABASE_URI = Config.DB_URI_TEMPLATE.format(PASSWORD)


class DeployConfig(Config):
    SECRET_KEY = 'another hard guess string'
    PASSWORD = 'ogre'
    SQLALCHEMY_DATABASE_URI = Config.DB_URI_TEMPLATE.format(PASSWORD)


config = {
    'dev': DevConfig,
    'deploy': DeployConfig,
    'default': DevConfig
}
