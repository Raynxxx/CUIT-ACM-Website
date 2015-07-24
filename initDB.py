# coding=utf-8
from dao.db import db
from flask import Flask
from dao.dbBase import  User
import config
from dao.dbACCOUNT import Account
from dao.dbSUBMIT import Submit
from dao.dbBook import Book, Borrowinfo
from dao.dbHonor import Honor, Certificate
from dao.dbArticle import  *
from dao.dbTag import Tag
from dao.dbNews import News

if __name__ == "__main__":
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(username='dreameracm',
                    name=u'祝志颖',
                    password='rootiszzy',
                    school=u'成都信息工程大学',
                    gender=True,
                    email='277507631@qq.com')
        user.rights = 7
        user.save()
        user = User(username='Rayn',
                    name=u'彭潇',
                    password='63005610',
                    school=u'成都信息工程大学',
                    gender=True,
                    email='414747795@qq.com')
        user.rights = 3
        user.save()
        user = User(username='jsp',
                    name=u'文欣',
                    password='123456',
                    school=u'成都信息工程大学',
                    gender=True,
                    email='2344325435@qq.com')
        user.rights = 1
        user.save()
