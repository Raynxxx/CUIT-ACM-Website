# coding=utf-8
from . import db, init_from_dict
from datetime import datetime


solution_tags = db.Table('solution_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', ondelete="CASCADE")),
    db.Column('solution_id', db.Integer, db.ForeignKey('solution_article.id', ondelete="CASCADE"))
)

solution_submits = db.Table('solution_submits',
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
    is_top = db.Column(db.SmallInteger, default=0)
    is_draft = db.Column(db.SmallInteger, default=0)

    # connect to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="SET NULL"),
                        nullable=True)
    user = db.relationship('User', backref=db.backref('solution', lazy='dynamic'))

    # connect to Tag
    tags = db.relationship('Tag', secondary=solution_tags,
                           backref=db.backref('solutions', lazy='dynamic'))


    def __init__(self, **kwargs):
        super(SolutionArticle, self).__init__()
        init_from_dict(self, **kwargs)
        self.last_update_time = datetime.now()

    def __repr__(self):
        return '<Article {0}>'.format(self.title)

    @property
    def serialize(self):
        dict_ = self.__dict__
        dict_.pop('_sa_instance_state', None)
        return dict_
