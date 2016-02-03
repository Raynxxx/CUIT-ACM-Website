# -*- coding: utf-8 -*-
from __init__ import *
from util import mdFilter
import datetime
from dao.db import db

# Table of Article
news_tags = db.Table('news_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', ondelete="CASCADE")),
    db.Column('news_id', db.Integer, db.ForeignKey('news.id', ondelete="CASCADE"))
)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=True)
    shortcut = db.Column(db.Text)
    content = db.Column(db.Text)
    last_update_time = db.Column(db.DateTime)
    is_top = db.Column(db.SmallInteger, default=0)
    is_draft = db.Column(db.SmallInteger, default=0)
    #rank = db.Column(db.Integer, default=0)

    # connect to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="SET NULL"),
                        nullable=True)
    user = db.relationship('User', backref=db.backref('news', cascade="save-update, merge",
                                                      lazy='dynamic'))
    # connect to Tag
    tags = db.relationship('Tag', secondary=news_tags, backref=db.backref('news', lazy='dynamic'))


    @property
    def md_shortcut(self):
        return mdFilter.markdown(self.shortcut)

    @md_shortcut.setter
    def md_shortcut(self, data):
        self.shortcut = data

    @property
    def md_content(self):
        return mdFilter.markdown(self.content)

    @md_content.setter
    def md_content(self, data):
        self.content = data

    def __init__(self, title, url, is_top, user):
        self.title = title
        self.url = url
        self.user = user
        self.is_top = is_top
        self.last_update_time = datetime.datetime.now()

    @property
    def serialize(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }

    def __repr__(self):
        return '<News>'


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()