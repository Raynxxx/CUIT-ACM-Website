# -*- coding: utf-8 -*-
from __init__ import *
from dao.db import db

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    certificate_url = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum('single','group'), default='single')


class Honor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acquire_year = db.Column(db.Integer, nullable=False)
    introduce = db.Column(db.Text)

    contest_name = db.Column(db.String(30), nullable=False)
    contest_level = db.Column(db.String(20), nullable=False)

    #rank = db.Column(db.Integer, default=0)
    # connect to Certificatem
    certificate_id = db.Column(db.Integer, db.ForeignKey('certificate.id'))
    certificate = db.relationship('Certificate', backref=db.backref('honor', lazy='dynamic'))

    # connect to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('honor', lazy='dynamic'))


    def __init__(self):
        pass


    def __repr__(self):
        return '<Honor>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()