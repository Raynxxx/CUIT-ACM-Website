# -*- coding: utf-8 -*-
from __init__ import *
from dbSUBMIT import Submit
from util import mdFilter
import urllib
import datetime
from sqlalchemy import or_

# Table of Article
newstags = db.Table('newstags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('news_id', db.Integer, db.ForeignKey('news.id'))
)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    shortcut = db.Column(db.Text)
    content = db.Column(db.Text)
    last_update_time = db.Column(db.DateTime)
    istop = db.Column(db.SmallInteger, default=0)
    #rank = db.Column(db.Integer, default=0)
    # connect to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('news', lazy='dynamic'))
    # connect to Tag
    tags = db.relationship('Tag', secondary=newstags,backref=db.backref('news', lazy='dynamic'))


    @property
    def mshortcut(self):
        return mdFilter.markdown(self.shortcut)

    @mshortcut.setter
    def mshortcut(self, data):
        self.shortcut = data

    @property
    def mcontent(self):
        return mdFilter.markdown(self.content)

    @mcontent.setter
    def mcontent(self, data):
        self.content = data

    def __init__(self, title, shortcut, content, url, istop, user):
        self.title = title
        self.shortcut = shortcut
        self.content = content
        self.url = url
        self.user = user
        self.istop = istop
        self.last_update_time = datetime.datetime.now()

    def __repr__(self):
        return '<News>'


    def save(self):
        db.session.add(self)
        db.session.commit()