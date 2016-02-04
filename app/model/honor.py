# coding=utf-8
from . import db, init_from_dict


honor_users = db.Table('honor_users',
    db.Column('honor_id', db.Integer, db.ForeignKey('honor.id', ondelete="CASCADE")),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
)

honor_resources = db.Table('honor_resources',
    db.Column('honor_id', db.Integer, db.ForeignKey('honor.id', ondelete="CASCADE")),
    db.Column('resource_id', db.Integer, db.ForeignKey('resource.id', ondelete="CASCADE"))
)


class Honor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contest_name = db.Column(db.String(512), nullable=False)
    contest_level = db.Column(db.Integer, nullable=False, default=0)
    acquire_time = db.Column(db.DateTime, nullable=False)
    team_name = db.Column(db.String(64))
    introduce = db.Column(db.Text)

    # connect to Resource
    resources = db.relationship('Resource', secondary=honor_resources,
                                backref=db.backref('honors', lazy='dynamic'))

    # connect to User
    users = db.relationship('User', secondary=honor_users,
                            backref=db.backref('honors', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(Honor, self).__init__()
        init_from_dict(self, **kwargs)

    def __repr__(self):
        return '<Honor {0}>'.format(self.contest_name)

    @property
    def serialize(self):
        dict_ = self.__dict__
        dict_.pop('_sa_instance_state', None)
        return dict_


def find_one(honor_id):
    return Honor.query.get(honor_id)


def find_all():
    return Honor.query.all()