# -*- coding: utf-8 -*-
from __init__ import *
from dao.db import db



class Honor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    acquire_time = db.Column(db.DateTime)
    introduce = db.Column(db.Text)
    type = db.Column(db.Enum('single','group'), default='single')
    contest_name = db.Column(db.String(64), nullable=False)
    contest_level = db.Column(db.Integer, nullable=False, default=0)

    #rank = db.Column(db.Integer, default=0)
    # connect to Resource
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id', ondelete="SET NULL"))
    resource = db.relationship('Resource', backref=db.backref('honor', lazy='dynamic'))

    # connect to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    user = db.relationship('User', backref=db.backref('honor', cascade="all, delete-orphan",  passive_deletes=True, lazy='dynamic'))


    def __init__(self):
        pass


    def __repr__(self):
        return '<Honor>@' + self.contest_name

    @property
    def serialize(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()