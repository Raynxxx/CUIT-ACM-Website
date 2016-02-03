from __init__ import *
from util import security
from datetime import datetime
from dao.db import db

class AccountStatus():
    NORMAL = 0
    NOT_INIT = 1
    WAIT_FOR_UPDATE = 2
    UPDATING = 3
    UPDATE_ERROR = 4
    ACCOUNT_ERROR = 5

# Table of Account
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(128))
    solved_or_rating = db.Column(db.Integer, nullable=False, default=0)
    submitted_or_max_rating = db.Column(db.Integer, nullable=False, default=0)
    update_status = db.Column(db.Integer, default=1, index=True)
    oj_name = db.Column(db.String(20), nullable=False)
    last_update_time = db.Column(db.DateTime)
    # connect to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"),
                        nullable=False)
    user = db.relationship('User', backref=db.backref('account', cascade="all, delete-orphan",
                                                      passive_deletes=True, lazy='dynamic'))

    def __init__(self, oj_name, nickname, password_or_oj_id, user):
        self.oj_name = oj_name
        self.nickname = nickname
        self.password = password_or_oj_id
        self.user = user
        self.last_update_time = datetime.min

    @property
    def password(self):
        return security.decrypt(self.password_hash).decode('utf-8')

    @password.setter
    def password(self, value):
        self.password_hash = security.encrypt(value.encode('utf-8'))

    def __repr__(self):
        return '<%s Account %s>: %d / %d' % (self.oj_name, self.nickname, self.solved_or_rating, self.submitted_or_max_rating)

    @property
    def serialize(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }

    def set_problem_count(self, v1, v2):
        self.solved_or_rating = v1
        self.submitted_or_max_rating = v2

    def get_problem_count(self):
        if self.oj_name in ['cf', 'bc']:
            return {'rating': self.solved_or_rating, 'max_rating': self.submitted_or_max_rating}
        else:
            return {'solved': self.solved_or_rating, 'submitted': self.submitted_or_max_rating}

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()