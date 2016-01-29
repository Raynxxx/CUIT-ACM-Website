# coding=utf-8
from . import db, init_from_dict
from app import login_manager
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, index=True, nullable=False)
    name = db.Column(db.String(25))
    password_hash = db.Column(db.String(128))
    stu_id = db.Column(db.String(20))
    gender = db.Column(db.Boolean)
    email = db.Column(db.String(65))
    phone = db.Column(db.String(15))
    remark = db.Column(db.String(1024))
    school = db.Column(db.String(64), nullable=False)
    college = db.Column(db.String(64))
    grade = db.Column(db.String(32))
    score = db.Column(db.Integer, default=0)
    current_week_submit = db.Column(db.Integer, default=0)
    current_week_solved = db.Column(db.Integer, default=0)
    last_week_submit = db.Column(db.Integer, default=0)
    last_week_solved = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime)
    rights = db.Column(db.Integer)
    active = db.Column(db.Integer, default=1)
    situation = db.Column(db.Text)
    apply_reason = db.Column(db.Text)

    def __init__(self, **kwargs):
        super(User, self).__init__()
        init_from_dict(self, **kwargs)
        self.create_time = datetime.now()

    def __repr__(self):
        return '<User {0} {1}>'.format(self.username, self.name)

    @property
    def serialize(self):
        dict_ = self.__dict__
        dict_.pop('_sa_instance_state', None)
        return dict_

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class AnonymousUser(AnonymousUserMixin):

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


