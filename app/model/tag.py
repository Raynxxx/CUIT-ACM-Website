# coding=utf-8
from . import db, init_from_dict


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

    def __init__(self, **kwargs):
        super(Tag, self).__init__()
        init_from_dict(self, **kwargs)

    def __repr__(self):
        return '<Tag {0}>'.format(self.name)

    @property
    def serialize(self):
        dict_ = self.__dict__
        dict_.pop('_sa_instance_state', None)
        return dict_


def find_one(tag_id):
    return Tag.query.get(tag_id)


def find_all():
    return Tag.query.all()