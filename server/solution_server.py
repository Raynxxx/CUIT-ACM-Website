# coding=utf-8
from __init__ import *
from dao.dbSolutionArticle import SolutionArticle
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


def post(form,user):
    has = SolutionArticle.query.filter(SolutionArticle.id == form.sid.data).first()
    tags = generate_tags(form.tags.data)
    if has and has.user != user and user.is_admin == 0:
        raise Exception(u'你没有权限修改该文章')
    if not has:
        has = SolutionArticle(form.title.data,form.shortcut.data,form.content.data,user)
    else:
        has.title = form.title.data
        has.mshortcut = form.shortcut.data
        has.mcontent = form.content.data
        has.last_update_time = datetime.datetime.now()
    oj = form.problem_oj_name.data
    pid = form.problem_pid.data
    has.problem_oj_name = oj
    has.problem_pid = pid
    has.tags = tags
    has.save()


def count():
    return SolutionArticle.query.count()


def get(offset=0, limit=20):
    return SolutionArticle.query.order_by(SolutionArticle.last_update_time.desc()).offset(offset).limit(limit)


def get_one(sid):
    return SolutionArticle.query.filter(SolutionArticle.id == sid).first_or_404()

def del_one(sid):
    one = SolutionArticle.query.filter(SolutionArticle.id == sid).first()
    if one:
        one.delete()
