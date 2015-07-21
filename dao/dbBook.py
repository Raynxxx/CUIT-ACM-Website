# -*- coding: utf-8 -*-
from __init__ import *
from dao.db import db
import datetime


class BookStatus():
    Normal = 0
    Borrowed = 1
    Forbid = 2
    Lost = 3

class BorrowStatus():
    Normal = 0
    Finished = 1
    TimeLimitExceed = 2

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    introduce = db.Column(db.Text)
    status = db.Column(db.Integer, default=0)
    shortcut = db.Column(db.String(100), nullable=True)
    borrow_count = db.Column(db.Integer, default=0)
    isbn = db.Column(db.String(100), nullable=False, index=True)
    last_borrow_time = db.Column(db.DateTime)
    #rank = db.Column(db.Integer, default=0)
    # connect to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('book', lazy='dynamic'))

    def __init__(self, name, intro, isbn, shortcut):
        self.name = name
        self.introduce = intro
        self.isbn = isbn
        self.shortcut = shortcut
        self.borrow_count = 0
        self.last_borrow_time = datetime.datetime.min
        self.status = BookStatus.Normal


    def __repr__(self):
        return '<BOOK>'


    def save(self):
        db.session.add(self)
        db.session.commit()

class Borrowinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrow_time = db.Column(db.DATETIME)
    return_time = db.Column(db.DATETIME)
    status = db.Column(db.Integer, default=0)
    # connect to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('borrowinfo', lazy='dynamic'))
    # connect to book
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book = db.relationship('Book', backref=db.backref('borrowinfo', lazy='dynamic'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()