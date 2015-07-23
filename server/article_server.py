# coding=utf-8
from __init__ import *
from dao.dbArticle import SolutionArticle
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

def post(form, user):
    has = SolutionArticle.query.filter(SolutionArticle.id == form.sid.data).first()
    tags = generate_tags(form.tags.data)
    if has and has.user != user and user.is_admin == 0:
        raise Exception(u'你没有权限修改该文章')
    if not has:
        has = SolutionArticle(form.title.data,form.shortcut.data,form.content.data,user)
    else:
        has.title = form.title.data
        has.md_shortcut = form.shortcut.data
        has.md_content = form.content.data
        has.last_update_time = datetime.datetime.now()
    oj = form.problem_oj_name.data
    pid = form.problem_pid.data
    has.problem_oj_name = oj
    has.problem_pid = pid
    has.tags = tags
    has.save()

def get_count():
    return SolutionArticle.query.count()

def get_list(offset=0, limit=20):
    return SolutionArticle.query.\
        order_by(SolutionArticle.last_update_time.desc()).\
        offset(offset).limit(limit)

def get_recent(limit=5):
    return get_list(0, limit)

def get_by_id(sid):
    return SolutionArticle.query.filter(SolutionArticle.id == sid).first_or_404()

def delete_by_id(sid):
    one = SolutionArticle.query.filter(SolutionArticle.id == sid).first()
    if one:
        one.delete()

def get_archive():
    archive = db.session\
        .query(SolutionArticle.last_update_time, SolutionArticle.title, SolutionArticle.url, SolutionArticle.is_top)\
        .filter(SolutionArticle.is_draft==0)\
        .order_by(SolutionArticle.is_top.desc(),SolutionArticle.last_update_time.desc())\
        .all()
    archives = dict()
    for article in archive:
        year = article.last_update_time.year
        if year not in archives:
            archives[year] = []
        archives[year].append(article)
    return archives

def get_archive_by_tag(tag):
    tag_row = Tag.query.filter(Tag.name==tag).first()
    if not tag_row:
        return None
    archive = tag_row.solutions\
        .filter(SolutionArticle.is_draft==0)\
        .order_by(SolutionArticle.is_top.desc(), SolutionArticle.last_update_time.desc())\
        .all()
    archives = dict()
    for article in archive:
        year = article.last_update_time.year
        if year not in archives:
            archives[year] = []
        archives[year].append(article)
    return archives
