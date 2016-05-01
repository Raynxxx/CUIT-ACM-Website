# coding=utf-8
from dao.db import db


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


def get_by_stu_and_name(stu_id, name):
    return Player.query.filter(Player.stu_id == stu_id)\
                        .filter(Player.name == name).first()


def get_list_pageable(page, per_page, search=None):
    query = Player.query
    if search:
        query = query.filter(Player.stu_id.like("%" + search + "%"))
    return query.order_by(Player.year.desc())\
                .paginate(page, per_page)


def create_player(player_form):
    has = Player.query.filter(Player.stu_id == player_form.stu_id)\
                        .filter(Player.name == player_form.name)\
                        .first()
    if has:
        return (u'已存在同名用户',)
    player = Player()
    player.stu_id = player_form.stu_id.data
    player.name = player_form.name.data
    player.gender = True if player_form.gender.data == '1' else False
    player.phone = player_form.phone.data
    player.email = player_form.email.data
    player.school = player_form.school.data
    player.college = player_form.college.data
    player.major = player_form.major.data
    player.grade = player_form.grade.data
    player.shirt_size = player_form.shirt_size.data
    player.save()
    return ('OK', player)

