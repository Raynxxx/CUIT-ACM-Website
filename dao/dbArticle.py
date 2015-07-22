# -*- coding: utf-8 -*-
from __init__ import *
from util import mdFilter
import datetime
from dao.db import db

# Table of Article
solutiontags = db.Table('solutiontags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('solution_id', db.Integer, db.ForeignKey('solution_article.id'))
)

solutionsubmits = db.Table('solutionsubmits',
    db.Column('submit_id', db.Integer, db.ForeignKey('submit.id')),
    db.Column('solution_id', db.Integer, db.ForeignKey('solution_article.id'))
)


class SolutionArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    shortcut = db.Column(db.Text)
    content = db.Column(db.Text)
    problem_oj_name = db.Column(db.String(20))
    problem_pid = db.Column(db.String(12))
    last_update_time = db.Column(db.DateTime)
    istop = db.Column(db.SmallInteger, default=0)
    isdraft = db.Column(db.SmallInteger, default=0)
    #rank = db.Column(db.Integer, default=0)
    # connect to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('solution', lazy='dynamic'))
    # connect to Tag
    tags = db.relationship('Tag', secondary=solutiontags,backref=db.backref('solutions', lazy='dynamic'))


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

    def __init__(self, title, shortcut, content, user):
        self.title = title
        self.shortcut = shortcut
        self.content = content
        self.user = user
        self.last_update_time = datetime.datetime.now()

    def __repr__(self):
        return '<Article>'


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()