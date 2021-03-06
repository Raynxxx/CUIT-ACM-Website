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
    has_news = News.query.filter(News.id == form.sid.data).with_lockmode('update').first()
    tags = generate_tags(form.tags.data)
    content_list = form.content.data.split('<-more->')
    if form.url.data == '':
        form.url.data = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    list_len = len(content_list)
    if list_len > 2:
        raise Exception(u'more标签的使用超过限制')
    if has_news and not user.is_admin and user != has_news.user:
        db.session.commit()
        raise Exception(u'没有权限')
    if not has_news:
        has_news = News(form.title.data, form.url.data, form.is_top.data, user)
    else:
        has_news.title = form.title.data
        has_news.url = form.url.data
        has_news.is_top = form.is_top.data
        has_news.last_update_time = datetime.now()
    if list_len == 1 :
        has_news.md_shortcut = content_list[0]
        has_news.md_content = ""
    elif content_list[0].strip() == "" :
        has_news.md_shortcut = content_list[1]
        has_news.md_content = ""
    else:
        has_news.md_shortcut = content_list[0]
        has_news.md_content = content_list[1]
    has_news.is_draft = is_draft
    has_news.tags = tags
    has_news.save()


def get_count(show_draft=False, coach=None):
    if show_draft and not coach:
        return News.query.count()
    elif show_draft and coach:
        return News.query.filter(News.user==coach).count()
    else:
        return News.query.filter(News.is_draft==0).count()


def get_list(offset=0, limit=10, show_draft=False):
    if show_draft:
        return News.query\
            .order_by(News.is_top.desc(), News.last_update_time.desc())\
            .offset(offset).limit(limit).all()
    else:
        return News.query.filter(News.is_draft == 0)\
            .order_by(News.is_top.desc(), News.last_update_time.desc())\
            .offset(offset).limit(limit).all()


def get_list_pageable(page, per_page, show_draft=False, search=None):
    query = News.query
    if not show_draft:
        query = query.filter(News.is_draft == 0)
    if search:
        query = query.filter(News.title.like('%' + search + '%'))
    return query.order_by(News.is_top.desc(), News.last_update_time.desc())\
                .paginate(page, per_page)


def get_recent(limit=5, sortTop = False):
    query = News.query.filter(News.is_draft==0)
    if sortTop:
        query = query.order_by(News.is_top.desc(), News.last_update_time.desc())
    else:
        query = query.order_by(News.last_update_time.desc())
    return query.offset(0).limit(limit).all()


def get_by_id(sid):
    return News.query.filter(News.id == sid).first_or_404()

def get_by_url(url):
    return News.query.filter(News.url == url).first_or_404()

def delete_by_id(sid):
    News.query.filter(News.id == sid).with_lockmode('update').delete()
    db.session.commit()

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
