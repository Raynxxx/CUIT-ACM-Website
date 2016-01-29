from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_from_dict(self, **kwargs):
    for key, value in kwargs.iteritems():
        setattr(self, key, value)
