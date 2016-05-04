# coding=utf-8
from dao.db import db
from datetime import datetime


SHIRT_SIZE = ['XS', 'S', 'M', 'L', 'XL', 'XXL']


class Player(db.Model):
    __bind_key__ = 'competitions'
    id = db.Column(db.Integer, primary_key=True)
    stu_id = db.Column(db.String(64))
    name = db.Column(db.String(64))
    gender = db.Column(db.Boolean)
    phone = db.Column(db.String(64))
    email = db.Column(db.String(512))
    school = db.Column(db.String(64))
    college = db.Column(db.String(64))
    major = db.Column(db.String(64))
    grade = db.Column(db.String(64))
    shirt_size = db.Column(db.String(16))
    time = db.Column(db.DateTime)

    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id', ondelete="CASCADE"),
                               nullable=False)
    competition = db.relationship('Competition', backref=db.backref('players',
                                                                    cascade="all, delete-orphan",
                                                                    passive_deletes=True,
                                                                    lazy='dynamic'))

    def __init__(self, name, stu_id):
        self.name = name
        self.stu_id = stu_id
        self.time = datetime.now()

    def __repr__(self):
        return '<Player {} {}>'.format(self.name, self.stu_id)

    @property
    def serialize(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def get_by_id(id):
    return Player.query.filter(Player.id == id).first()


def get_by_stu(stu_id):
    return Player.query.filter(Player.stu_id == stu_id).first()


def delete_by_id(id):
    player = get_by_id(id)
    player.delete()


def get_list_pageable(page, per_page, search=None):
    query = Player.query
    if search:
        query = query.filter(Player.stu_id.like("%" + search + "%"))
    return query.order_by(Player.year.desc())\
                .paginate(page, per_page)


def create_player(player_form, competition):
    has = competition.players.filter(Player.stu_id == player_form.stu_id.data).first()
    if has:
        return u'此学号已经报名成功, 如有疑问请咨询校队负责人.'
    player = Player(player_form.name.data, player_form.stu_id.data)
    player.gender = True if player_form.gender.data == '1' else False
    player.phone = player_form.phone.data
    player.email = player_form.email.data
    #player.school = player_form.school.data
    player.college = player_form.college.data
    player.major = player_form.major.data
    player.grade = player_form.grade.data
    player.shirt_size = player_form.shirt_size.data
    player.competition = competition
    player.save()
    return 'OK'

