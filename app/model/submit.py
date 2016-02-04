# coding=utf-8
from . import db, init_from_dict


class Submit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pro_id = db.Column(db.String(12))
    run_id = db.Column(db.String(20))
    submit_time = db.Column(db.DateTime, index=True)
    run_time = db.Column(db.Integer)
    memory = db.Column(db.Integer)
    lang = db.Column(db.String(50))
    result = db.Column(db.String(100))
    code = db.Column(db.Text)
    update_status = db.Column(db.Integer)
    oj_name = db.Column(db.String(20), nullable=False)
    user_name = db.Column(db.String(25),nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id',  ondelete="CASCADE"))
    user = db.relationship('User', backref=db.backref('submit',
                                                      cascade="all, delete-orphan",
                                                      passive_deletes=True,
                                                      lazy='dynamic'))

    def __init__(self, **kwargs):
        super(Submit, self).__init__()
        init_from_dict(self, **kwargs)
        self.update_status = 0

    def __repr__(self):
        return u'<Submit user: {0} \tpid: {1} \trun_id: {2}'.format(
                    self.user_name, self.pro_id, self.run_id)

    @property
    def serialize(self):
        dict_ = self.__dict__
        dict_.pop('_sa_instance_state', None)
        return dict_


def find_one(submit_id):
    return Submit.query.get(submit_id)


def find_all():
    return Submit.query.all()