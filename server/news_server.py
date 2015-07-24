# coding=utf-8
from __init__ import *
from dao.dbNews import News
from dao.dbTag import Tag

def generate_tags(data):
    tag_list = []
    for tag in data:
        if tag == '':
            continue
        has_tag = Tag.query.filter(Tag.name == tag).first()
        if not has_tag:
            new_tag = Tag(tag)
            new_tag.save()
            tag_list.append(new_tag)
        else:
            tag_list.append(has_tag)
    return tag_list

def post(form, user, is_draft):
    has_news = News.query.filter(News.id == form.sid.data).first()
    tags = generate_tags(form.tags.data)
    if has_news and not user.is_admin and user != has_news.user:
        raise Exception(u'没有权限')
    if not has_news:
        has_news = News(form.title.data,form.shortcut.data,form.content.data, form.url.data, form.is_top.data, user)
    else:
        has_news.title = form.title.data
        has_news.md_shortcut = form.shortcut.data
        has_news.md_content = form.content.data
        has_news.url = form.url.data
        has_news.is_top = form.is_top.data
        has_news.last_update_time = datetime.datetime.now()
    has_news.is_draft = is_draft
    has_news.tags = tags
    has_news.save()

def get_count(show_draft=False):
    return News.query.count() if show_draft else News.query.filter(News.is_draft==0).count()

def get_list(offset=0, limit=10, show_draft=False):
    if show_draft:
        return News.query\
            .order_by(News.is_top.desc(), News.last_update_time.desc())\
            .offset(offset).limit(limit).all()
    else:
        return News.query.filter(News.is_draft==0)\
            .order_by(News.is_top.desc(), News.last_update_time.desc())\
            .offset(offset).limit(limit).all()

def get_recent(limit=5):
    return News.query.filter(News.is_draft==0)\
            .order_by(News.last_update_time.desc())\
            .offset(0).limit(limit).all()

def get_by_id(sid):
    return News.query.filter(News.id == sid).first_or_404()

def get_by_url(url):
    return News.query.filter(News.url == url).first_or_404()

def delete_by_id(sid):
    one = News.query.filter(News.id == sid).first()
    if one:
        one.delete()

def get_archive():
    archive = db.session\
        .query(News.last_update_time, News.title, News.url, News.is_top)\
        .filter(News.is_draft==0)\
        .order_by(News.is_top.desc(),News.last_update_time.desc())\
        .all()
    archives = dict()
    for news in archive:
        year = news.last_update_time.year
        if year not in archives:
            archives[year] = []
        archives[year].append(news)
    return archives

def get_archive_by_tag(tag):
    tag_row = Tag.query.filter(Tag.name==tag).first()
    if not tag_row:
        return None
    archive = tag_row.news\
        .filter(News.is_draft==0)\
        .order_by(News.is_top.desc(),News.last_update_time.desc())\
        .all()
    archives = dict()
    for news in archive:
        year = news.last_update_time.year
        if year not in archives:
            archives[year] = []
        archives[year].append(news)
    return archives

def get_all_tags():
    tags_row = Tag.query.filter(Tag.news!=None).all()
    tags = []
    for tag in tags_row:
        if tag.news.filter(News.is_draft==0).count():
            tags.append(tag)
    return tags
