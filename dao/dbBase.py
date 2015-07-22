from __init__ import *
from __init__ import *
from flask.ext.login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from dao.dbSUBMIT import Submit
import hashlib, datetime
from sqlalchemy import or_
from dao.db import db


# Table of Team Member
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, index=True, nullable=False)
    name = db.Column(db.String(25))
    password_hash = db.Column(db.String(128))
    stu_id = db.Column(db.String(20))
    gender = db.Column(db.Boolean)
    email = db.Column(db.String(65))
    phone = db.Column(db.String(15))
    remark = db.Column(db.String(50))
    school = db.Column(db.String(20), nullable=False)
    situation = db.Column(db.String(50))
    score = db.Column(db.Integer, default=0)
    current_week_submit = db.Column(db.Integer, default=0)
    current_week_solved = db.Column(db.Integer, default=0)
    last_week_submit = db.Column(db.Integer, default=0)
    last_week_solved = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime)
    rights = db.Column(db.Integer)
    active = db.Column(db.Integer, default=1)

    def __init__(self, username,name, password, school, gender, email):
        self.username = username
        self.name = name
        self.password = password
        self.school = school
        self.gender = gender
        self.email = email
        self.create_time = datetime.datetime.now()
        self.rights = 0

    def __repr__(self):
        return '<User %s>' % self.name

    @property
    def serialize(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }

    @property
    def is_admin(self):
        return self.rights & 4 == 4

    @property
    def is_coach(self):
        return self.rights & 2 == 2

    @property
    def is_student(self):
        return self.rights & 1 == 1

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    def update_score(self):
        score = 0
        if self.account:
            accounts = self.account.all()
            for account in accounts:
                if account.oj_name in ['cf', 'bc']:
                    tmp = account.get_problem_count()
                    score += tmp['rating']*0.6 + tmp['max_rating']*0.2
                else:
                    tmp = account.get_problem_count()
                    score += tmp['solved']*0.4
        self.score = score

    def update(self):
        now = datetime.datetime.now()
        permit_date = now - datetime.timedelta(days=now.weekday())
        permit_date = permit_date.replace(hour=0, minute=0, second=0)
        permit_date1 = permit_date - datetime.timedelta(days=7)
        last_submitted = self.submit.filter(Submit.submit_time < permit_date, Submit.submit_time > permit_date1)
        last_solved = last_submitted.filter(or_(Submit.result == 'OK', Submit.result == 'Accepted'))
        current_submitted = self.submit.filter(Submit.submit_time > permit_date)
        current_solved = current_submitted.filter(or_(Submit.result == 'OK', Submit.result == 'Accepted'))
        self.last_week_solved = last_solved.count()
        self.last_week_submit = last_submitted.count()
        self.current_week_solved = current_solved.count()
        self.current_week_submit = current_submitted.count()
        self.update_score()


    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'http://gravatar.duoshuo.com/avatar'
        hash = hashlib.md5(self.name.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()