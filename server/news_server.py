# coding=utf-8
from __init__ import *
from dao.dbNews import News
from dao.dbTag import Tag

def generate_tags(data):
    taglist = []
    for tag in data:
        if tag == '':
            continue
        htag = Tag.query.filter(Tag.name == tag).first()
        if not htag:
            ntag = Tag(tag)
            ntag.save()
            taglist.append(ntag)
        else:
            taglist.append(htag)
    return taglist


def post(form, user):
    has = News.query.filter(News.id == form.sid.data).first()
    tags = generate_tags(form.tags.data)
    if has and has.user != user and user.is_admin == 0:
        raise Exception(u'没有权限')
    if not has:
        has = News(form.title.data,form.shortcut.data,form.content.data, form.url.data, form.istop.data, user)
    else:
        has.title = form.title.data
        has.mshortcut = form.shortcut.data
        has.mcontent = form.content.data
        has.url = form.url.data
        has.istop = form.istop.data
        has.last_update_time = datetime.datetime.now()
    has.tags = tags
    has.save()


def count():
    return News.query.count()


def get(offset=0, limit=10):
    return News.query.order_by(News.last_update_time.desc()).offset(offset).limit(limit)


def get_one(sid):
    return News.query.filter(News.id == sid).first_or_404()

def get_one_by_url(url):
    return News.query.filter(News.url == url).first_or_404()

def del_one(sid):
    one = News.query.filter(News.id == sid).first()
    if one:
        db.session.delete(one)
        db.session.commit()