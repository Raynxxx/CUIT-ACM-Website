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
        has.last_update_time = datetime.now()
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
    has.is_top = form.is_top.data
    has.is_draft = is_draft
    has.problem_oj_name = oj
    has.problem_pid = pid
    has.tags = tags
    has.save()


def filter_query(query_type=None, keyword=''):
    if query_type == 'title' and keyword != '':
        query = SolutionArticle.query.filter(SolutionArticle.title.like('%' + keyword + '%'))
    elif query_type == 'tag' and keyword != '':
        tag_row = Tag.query.filter(Tag.name==keyword).first()
        query = tag_row.solutions if tag_row else None
    else:
        query = SolutionArticle.query
    return query

def get_list(offset=0, limit=20, user=None, query_type=None, keyword=''):
    if not user:
        query = filter_query(query_type, keyword)
        return query.filter(SolutionArticle.is_draft==0).\
            order_by(SolutionArticle.is_top.desc(), SolutionArticle.last_update_time.desc()).\
            offset(offset).limit(limit).all() if query else []
    elif user.is_admin:
        return SolutionArticle.query.\
            order_by(SolutionArticle.is_top.desc(), SolutionArticle.last_update_time.desc()).\
            offset(offset).limit(limit).all()
    elif user.is_coach:
        return SolutionArticle.query.join(SolutionArticle.user)\
            .filter(User.school==user.school, User.rights < 4).\
            order_by(SolutionArticle.is_top.desc(), SolutionArticle.last_update_time.desc()).\
            offset(offset).limit(limit).all()
    else:
        return SolutionArticle.query.filter(SolutionArticle.user==user).\
            order_by(SolutionArticle.is_top.desc(), SolutionArticle.last_update_time.desc()).\
            offset(offset).limit(limit).all()

def get_count(user=None, query_type=None, keyword=''):
    if not user:
        query = filter_query(query_type, keyword)
        return query.filter(SolutionArticle.is_draft==0).\
            order_by(SolutionArticle.is_top.desc(), SolutionArticle.last_update_time.desc()).\
            count() if query else 0
    elif user.is_admin:
        return SolutionArticle.query.\
            order_by(SolutionArticle.is_top.desc(), SolutionArticle.last_update_time.desc()).\
            count()
    elif user.is_coach:
        return SolutionArticle.query.join(SolutionArticle.user)\
            .filter(User.school==user.school, User.rights < 4).\
            order_by(SolutionArticle.is_top.desc(), SolutionArticle.last_update_time.desc()).\
            count()
    else:
        return SolutionArticle.query.filter(SolutionArticle.user==user).\
            order_by(SolutionArticle.is_top.desc(), SolutionArticle.last_update_time.desc()).\
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

def get_all_tags():
    tags_row = Tag.query.filter(Tag.solutions!=None).all()
    tags = []
    for tag in tags_row:
        if tag.solutions.filter(SolutionArticle.is_draft==0).count():
            tags.append(tag)
    return tags

def related_submits(article, offset=0, limit=10):
    if article.problem_oj_name == '' or article.problem_pid == '':
        return []
    query = Submit.query.filter(Submit.oj_name==article.problem_oj_name,Submit.pro_id==article.problem_pid)\
        #filter(or_(Submit.result == 'OK', Submit.result == 'Accepted')).all()
    return query.offset(offset).limit(limit).all()

def related_submits_count(article):
    if article.problem_oj_name == '' or article.problem_pid == '':
        return 0
    query = Submit.query.filter(Submit.oj_name==article.problem_oj_name,Submit.pro_id==article.problem_pid)\
        #filter(or_(Submit.result == 'OK', Submit.result == 'Accepted')).all()
    return query.count()
