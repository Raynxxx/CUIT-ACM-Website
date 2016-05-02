# coding=utf-8
from dao.db import db
from flask import Flask
from dao.dbBase import  User
import config
from dao.dbACCOUNT import Account
from dao.dbSUBMIT import Submit
from dao.dbResource import Resource
from dao.dbHonor import Honor

from dao.dbArticle import  *
from dao.dbTag import Tag
from dao.dbNews import News
from dao.dbCompetition import Competition, CompetitionPlayer
from dao.dbPlayer import Player

if __name__ == "__main__":
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    with app.app_context():
        db.drop_all(bind=['competitions'])
        db.create_all(bind=['competitions'])

