# -*- coding: utf-8 -*-
from __init__ import *
from util import mdFilter
from dao.db import db

honor_users = db.Table('honor_users',
    db.Column('honor_id', db.Integer, db.ForeignKey('honor.id', ondelete="CASCADE")),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
)

honor_resources = db.Table('honor_resources',
    db.Column('honor_id', db.Integer, db.ForeignKey('honor.id', ondelete="CASCADE")),
    db.Column('resource_id', db.Integer, db.ForeignKey('resource.id', ondelete="CASCADE"))
)

class Honor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contest_name = db.Column(db.String(64), nullable=False)
    contest_level = db.Column(db.Integer, nullable=False, default=0)
    acquire_time = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.Enum('single', 'group'), default='single')
    introduce = db.Column(db.Text)

    # connect to Resource
    resources = db.relationship('Resource', secondary=honor_resources ,backref=db.backref('honors', lazy='dynamic'))

    # connect to User
    users = db.relationship('User', secondary=honor_users,backref=db.backref('honors', lazy='dynamic'))

    def __init__(self):
        pass


    def __repr__(self):
        return '<Honor>@' + self.contest_name

    @property
    def md_introduce(self):
        return mdFilter.markdown(self.introduce)

    @md_introduce.setter
    def md_introduce(self, data):
        self.introduce = data

    @property
    def serialize(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()