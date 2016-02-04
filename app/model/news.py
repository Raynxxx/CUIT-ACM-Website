# coding=utf-8
from . import db, init_from_dict
from datetime import datetime


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

    # connect to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',  ondelete="SET NULL"))
    user = db.relationship('User', backref=db.backref('news', lazy='dynamic'))

    # connect to Tag
    tags = db.relationship('Tag', secondary=news_tags,
                           backref=db.backref('news', lazy='dynamic'))


    def __init__(self, **kwargs):
        super(News, self).__init__()
        init_from_dict(self, **kwargs)
        self.last_update_time = datetime.now()

    def __repr__(self):
        return '<News {0}>'.format(self.title)

    @property
    def serialize(self):
        dict_ = self.__dict__
        dict_.pop('_sa_instance_state', None)
        return dict_

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def find_one(news_id):
    return News.query.get(news_id)


def find_all():
    return News.query.all()