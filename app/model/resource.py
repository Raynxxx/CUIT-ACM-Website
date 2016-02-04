# coding=utf-8
from . import db, init_from_dict


class ResourceLevel():
    PUBLIC = 0
    SHARED = 1
    PRIVATE = 2


class ResourceUsage():
    BOOK_RES = 0
    HONOR_RES = 1
    NEWS_RES = 2
    BLOG_RES = 3
    OTHER_RES = 4


class ResourceType:
    TEXT = 0
    DOCUMENTS = 1
    DATA = 2
    IMAGES = 3
    ARCHIVES = 4
    OTHER = 5


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True, default='UNTITLED')
    description = db.Column(db.Text)
    type = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False, default=ResourceLevel.PRIVATE)
    usage = db.Column(db.Integer, nullable=False, default=ResourceUsage.OTHER_RES)
    upload_time = db.Column(db.DateTime)

    # connect to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="SET NULL"),
                        nullable=True)
    user = db.relationship('User', backref=db.backref('resource', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(Resource, self).__init__()
        init_from_dict(self, **kwargs)

    def __repr__(self):
        return '<Resource {1}>'.format(self.name)

    @property
    def serialize(self):
        dict_ = self.__dict__
        dict_.pop('_sa_instance_state', None)
        return dict_

    @property
    def file_type(self):
        return unicode(self.filename).split('.')[-1]


def find_one(res_id):
    return Resource.query.get_or_404(res_id)


def find_all():
    return Resource.query.all()