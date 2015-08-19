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

def post(form, user, is_draft):
    has = SolutionArticle.query.filter(SolutionArticle.id == form.sid.data).first()
    tags = generate_tags(form.tags.data)
    content_list = form.content.data.split('<-more->')
    list_len = len(content_list)
    if list_len > 2:
        raise Exception(u'more标签的使用超过限制')
    if has and has.user != user and user.is_admin == 0:
        raise Exception(u'你没有权限修改该文章')
    if not has:
        has = SolutionArticle(form.title.data,user)
    else:
        has.title = form.title.data
        has.last_update_time = datetime.datetime.now()
    if list_len == 1 :
        has.md_shortcut = content_list[0]
        has.md_content = ""
    elif content_list[0].strip() == "" :
        has.md_shortcut = content_list[1]
        has.md_content = ""
    else:
        has.md_shortcut = content_list[0]
        has.md_content = content_list[1]
    oj = form.problem_oj_name.data
    pid = form.problem_pid.data
    has.is_draft = is_draft
    has.problem_oj_name = oj
    has.problem_pid = pid
    has.tags = tags
    has.save()

def get_list(offset=0, limit=20,user=None):
    if not user:
        return SolutionArticle.query.filter(SolutionArticle.is_draft==0).\
            order_by(SolutionArticle.last_update_time.desc()).\
            offset(offset).limit(limit).all()
    elif user.is_admin:
        return SolutionArticle.query.\
            order_by(SolutionArticle.last_update_time.desc()).\
            offset(offset).limit(limit).all()
    elif user.is_coach:
        return SolutionArticle.query.join(SolutionArticle.user)\
            .filter(User.school==user.school, User.rights < 4).\
            order_by(SolutionArticle.last_update_time.desc()).\
            offset(offset).limit(limit).all()
    else:
        return SolutionArticle.query.filter(SolutionArticle.user==user).\
            order_by(SolutionArticle.last_update_time.desc()).\
            offset(offset).limit(limit).all()

def get_count(user=None):
    if not user:
        return SolutionArticle.query.filter(SolutionArticle.is_draft==0).\
            order_by(SolutionArticle.last_update_time.desc()).\
            count()
    elif user.is_admin:
        return SolutionArticle.query.\
            order_by(SolutionArticle.last_update_time.desc()).\
            count()
    elif user.is_coach:
        return SolutionArticle.query.join(SolutionArticle.user)\
            .filter(User.school==user.school, User.rights < 4).\
            order_by(SolutionArticle.last_update_time.desc()).\
            count()
    else:
        return SolutionArticle.query.filter(SolutionArticle.user==user).\
            order_by(SolutionArticle.last_update_time.desc()).\
            count()

def get_recent(limit=5):
    return get_list(0, limit)

def get_by_id(sid):
    return SolutionArticle.query.filter(SolutionArticle.id == sid).first_or_404()

def delete_by_id(sid):
   SolutionArticle.query.filter(SolutionArticle.id == sid).with_lockmode('update').delete()
   db.session.commit()

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
