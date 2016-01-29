# coding=utf-8
from . import db, init_from_dict
from ..util import security
from datetime import datetime

class AccountStatus:
    NORMAL = 0
    NOT_INIT = 1
    WAIT_FOR_UPDATE = 2
    UPDATING = 3
    UPDATE_ERROR = 4
    ACCOUNT_ERROR = 5


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
    user = db.relationship('User', backref=db.backref('account',
                                                      cascade="all, delete-orphan",
                                                      passive_deletes=True,
                                                      lazy='dynamic'))

    def __init__(self, **kwargs):
        super(Account, self).__init__()
        init_from_dict(self, **kwargs)
        self.last_update_time = datetime.min

    def __repr__(self):
        return '<Account {0} / {1}>: {2} / {3}'.format(self.oj_name, self.nickname,
                                                       self.solved_or_rating,
                                                       self.submitted_or_max_rating)

    @property
    def serialize(self):
        dict_ = self.__dict__
        dict_.pop('_sa_instance_state', None)
        return dict_

    @property
    def password(self):
        return security.decrypt(self.password_hash).decode('utf-8')

    @password.setter
    def password(self, password):
        self.password_hash = security.encrypt(password.encode('utf-8'))



