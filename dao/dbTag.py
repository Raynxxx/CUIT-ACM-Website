from __init__ import *
from dao.db import db

# Table of Tag
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    @property
    def serialize(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
