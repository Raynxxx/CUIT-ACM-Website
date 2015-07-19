# coding=utf-8
from flask import Flask
from dao.dbBase import db, User
import config
from dao.dbACCOUNT import Account
from dao.dbSUBMIT import Submit
from dao.dbBook import Book, Borrowinfo
from dao.dbHonor import Honor, Certificate
from dao.dbArticle import  *
from dao.dbTag import Tag

if __name__ == "__main__":
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(username='dreameracm',
                    name='祝志颖'.decode('utf-8'),
                    password='rootiszzy',
                    stu_id='2012045008',
                    gender=True,
                    email='277507631@qq.com')
        user.rights = 1
        user.save()
