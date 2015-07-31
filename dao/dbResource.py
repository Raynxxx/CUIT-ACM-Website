from dao.db import db


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, default='UNTITLED')
    description = db.Column(db.Text)
    upload_time = db.Column(db.DateTime)

    # connect to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',  ondelete="SET NULL"))
    user = db.relationship('User', backref=db.backref('resource', lazy='dynamic'))

    def __repr__(self):
        return '<Resource>@' + self.name


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()