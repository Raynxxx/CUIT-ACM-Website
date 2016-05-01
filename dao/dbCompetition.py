# coding=utf-8
from sqlalchemy import or_, and_
from dao.db import db
from dao.dbPlayer import Player

competition_player = db.Table(
    'competition_player',
    db.Column('competition_id', db.Integer, db.ForeignKey('competition.id', ondelete="CASCADE")),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id', ondelete="CASCADE")),
    info={'bind_key': 'competitions'}
)

class Competition(db.Model):
    __bind_key__ = 'competitions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    oj_cid = db.Column(db.String(64))
    event_date = db.Column(db.DateTime)
    description = db.Column(db.Text)

    players = db.relationship('Player', secondary=competition_player, lazy='dynamic',
                              backref=db.backref('competitions', lazy='dynamic'))


    def __repr__(self):
        return '<Competition {} {}>'.format(self.title, self.year)

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
    return Competition.query.filter(Competition.id == id).first()


def get_by_year(year):
    return Competition.query.filter(Competition.year == year).first()


def get_list_pageable(page, per_page, search=None):
    query =  Competition.query
    if search:
        query = query.filter(Competition.title.like("%" + search + "%"))
    return query.order_by(Competition.year.desc())\
                .paginate(page, per_page)


def get_players_pageable(competition, page, per_page, search=None):
    query = competition.players
    if search:
        query = query.filter(or_(Player.stu_id.like("%" + search + "%"),
                                 Player.name.like("%" + search + "%")))
    return query.order_by(Player.id.desc())\
                .paginate(page, per_page)


def create_competition(competition_form):
    has = Competition.query.filter(or_(Competition.year == competition_form.year.data,
                                       Competition.title == competition_form.title.data))\
                            .first()
    if has:
        return u'已存在同名的比赛或者同年的比赛'
    competition = Competition()
    competition.title = competition_form.title.data
    competition.year = competition_form.year.data
    competition.event_date = competition_form.event_date.data
    competition.description = competition_form.description.data
    competition.players = []
    competition.save()
    return 'OK'


def delete_by_id(id):
    competition = get_by_id(id)
    competition.delete()


def create_join(competition, player):
    if player in competition.players:
        return u'你的报名信息已被采集，请勿重复提交'
    competition.players.append(player)
    competition.save()
    return 'OK'


def delete_join(competition, player):
    competition.players.remove(player)
    competition.save()
    return 'OK'
