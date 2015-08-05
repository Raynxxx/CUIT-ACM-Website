from dao.db import db

class ResourceLevel():
    PUBLIC = 0
    SHARED = 1
    PRIVATE = 2


class ResourceUsage():
    BOOK_RES = 0
    HONOR_RES = 1
    NEWS_RES = 2
    SOLUTION_RES = 3
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="SET NULL"))
    user = db.relationship('User', backref=db.backref('resource', lazy='dynamic'))

    def __repr__(self):
        return '<Resource>@' + self.name.encode('utf-8')

    @property
    def file_type(self):
        return unicode(self.filename).split('.')[-1]

    @property
    def serialize(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()