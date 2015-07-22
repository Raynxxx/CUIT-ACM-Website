from __init__ import *
from dao.db import db

class Submit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pro_id = db.Column(db.String(12))
    run_id = db.Column(db.String(20))
    submit_time = db.Column(db.DateTime, index=True)
    run_time = db.Column(db.Integer)
    memory = db.Column(db.Integer)
    lang = db.Column(db.String(20))
    result = db.Column(db.String(100))
    code = db.Column(db.Text)
    update_status = db.Column(db.Integer)
    oj_name = db.Column(db.String(20), nullable=False)
    user_name = db.Column(db.String(25),nullable=True)
    # connect to Account

    user_id = db.Column(db.Integer, db.ForeignKey('user.id',  ondelete="CASCADE"))
    user = db.relationship('User', backref=db.backref('submit', cascade="all, delete-orphan",  passive_deletes=True, lazy='dynamic'))

    def __init__(self, pro_id, account):
        self.pro_id = pro_id
        self.user = account.user
        self.oj_name = account.oj_name
        self.user_name = account.user.name
        self.update_status = 0

    @property
    def serialize(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }

    def update_info(self,run_id,submit_time, run_time, memory,lang,code,result):
        self.code = code
        self.run_id = run_id
        self.submit_time = submit_time
        self.run_time = run_time
        self.memory = memory
        self.lang = lang
        self.result = result
        self.save()

    def __repr__(self):
        return u'User:"{0}" \tProblemID : {1} \tRUNID : {2}'.format(self.user_name, self.pro_id, self.run_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


