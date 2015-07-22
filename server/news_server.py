# coding=utf-8
from __init__ import *
from dao.dbNews import News
from dao.dbTag import Tag

def generate_tags(data):
    tag_list = []
    for tag in data:
        if tag == '':
            continue
        htag = Tag.query.filter(Tag.name == tag).first()
        if not htag:
            ntag = Tag(tag)
            ntag.save()
            tag_list.append(ntag)
        else:
            tag_list.append(htag)
    return tag_list


def post_news(form, user, is_draft):
    has = News.query.filter(News.id == form.sid.data).first()
    tags = generate_tags(form.tags.data)
    if has and not user.is_admin and user != has.user:
        raise Exception(u'没有权限')
    if not has:
        has = News(form.title.data,form.shortcut.data,form.content.data, form.url.data, form.is_top.data, user)
    else:
        has.title = form.title.data
        has.md_shortcut = form.shortcut.data
        has.md_content = form.content.data
        has.url = form.url.data
        has.is_top = form.is_top.data
        has.last_update_time = datetime.datetime.now()
    has.is_draft = is_draft
    has.tags = tags
    has.save()


def count():
    return News.query.count()


def get(offset=0, limit=10, show_draft=False):
    if show_draft:
        return News.query\
            .order_by(News.is_top.desc(), News.last_update_time.desc())\
            .offset(offset).limit(limit)
    else:
        return News.query.filter(News.is_draft==0)\
            .order_by(News.is_top.desc(), News.last_update_time.desc())\
            .offset(offset).limit(limit)

def get_archive():
    archive = db.session\
        .query(News.last_update_time, News.title, News.url, News.is_top)\
        .filter(News.is_draft==0)\
        .order_by(News.is_top.desc(),News.last_update_time.desc())\
        .all()
    return archive

def get_archive_by_tag(tag):
    tag_row = Tag.query.filter(Tag.name==tag).first()
    if not tag_row:
        return None
    print 'hrer'
    return tag_row.news.filter(News.is_draft==0).order_by(News.is_top.desc(),News.last_update_time.desc()).all()


def get_one(sid):
    return News.query.filter(News.id == sid).first_or_404()

def get_one_by_url(url):
    return News.query.filter(News.url == url).first_or_404()

def del_one(sid):
    one = News.query.filter(News.id == sid).first()
    if one:
        one.delete()