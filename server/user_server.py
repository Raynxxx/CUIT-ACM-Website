# coding=utf-8
from __init__ import *
from config import OJ_MAP, SCHOOL_MAP
from sqlalchemy import or_


def create_user(user_form, user_rights):
    has_user = User.query.filter_by(username=user_form.username.data).first()
    if has_user:
        return u"该用户名已经存在"
    new_user = User(username = user_form.username.data,
                name = user_form.name.data,
                password = user_form.password.data,
                school = user_form.school.data,
                gender = True if user_form.gender.data == '1' else False,
                email = user_form.email.data)
    new_user.college = user_form.college.data
    new_user.grade = user_form.grade.data
    new_user.apply_reason = user_form.apply_reason.data
    new_user.rights = user_rights
    new_user.stu_id = user_form.stu_id.data
    new_user.phone = user_form.phone.data
    new_user.save()
    return 'OK'

def create_many_users(user_form, current_user):
    success_count = 0
    try:
        for info in user_form.user_info.data.split(';'):
            data = info.split(',')
            if len(data) < 4:
                continue
            try:
                new_user = User(username=data[0],
                                name = data[1],
                                password=data[2],
                                school=current_user.school,
                                gender=True if data[3] == '1' else False,
                                email=None)
                new_user.rights = 1
                new_user.save()
                success_count += 1
            except:
                pass
        return '{0} user added'.format(success_count)
    except Exception, e:
        return 'failed'

def update_apply(user_id, opt):
    has_user = User.query.filter_by(id = user_id).with_lockmode('update').first()
    if not has_user:
        db.session.commit()
        return u"该用户不存在"
    if opt == "accept":
        has_user.rights = 1
        has_user.save()
        return "OK"
    elif opt == "reject":
        has_user.delete()
        return "OK"
    else :
        return u"该操作不支持"


def update_user(user_form, user_rights = 0, for_self = False):
    has_user = User.query.filter_by(id = user_form.id.data).with_lockmode('update').first()
    if not has_user:
        db.session.commit()
        return u"该用户不存在"
    if has_user.is_admin:
        user_rights = user_rights | 4
    has_user.name = user_form.name.data
    has_user.school = user_form.school.data
    has_user.college = user_form.college.data
    has_user.grade = user_form.grade.data
    has_user.gender = True if user_form.gender.data == '1' else False
    has_user.email = user_form.email.data
    if not for_self:
        has_user.rights = user_rights
        has_user.active = int(user_form.active.data)
        has_user.situation = user_form.situation.data
    has_user.stu_id = user_form.stu_id.data
    has_user.phone = user_form.phone.data
    has_user.remark = user_form.motto.data
    has_user.save()
    return 'OK'


def delete_by_id(user_id):
    User.query.filter_by(id=user_id).with_lockmode('update').delete()
    db.session.commit()


def get_by_id(user_id):
    return  User.query.filter_by(id=user_id).first()


def get_by_username_or_404(username):
    return User.query.filter_by(username=username).first_or_404()


def get_by_username(username):
    return User.query.filter_by(username=username).first()


def get_user_choice():
    users = db.session.query(User.username, User.name).all()
    return [(user[0], user[1]) for user in users]


def get_list(offset=0, limit=20, school=None, isApply=False):
    if not isApply:
        if not school:
            users = User.query.filter(User.rights < 8)
        else:
            users = User.query.filter(User.school==school, User.rights < 4)
    else:
        if not school:
            users = User.query.filter(User.rights >= 8)
        else:
            users = User.query.filter(User.school==school, User.rights >= 8, User.rights < 12)
    if offset == 0 and limit == -1:
        users = users.order_by(User.rights.desc()).all()
    else:
        users = users.order_by(User.rights.desc()).offset(offset).limit(limit).all()
    return users


def get_list_pageable(page, per_page, school=None, is_apply=False, search=None):
    query = User.query
    if school:
        query = query.filter(User.school == school)
    if is_apply:
        query = query.filter(User.rights >= 8)
    else:
        query = query.filter(User.rights < 4) if school else query.filter(User.rights < 8)
    if search:
        query = query.filter( or_(User.name.like("%" + search + "%"),
                                  User.username.like("%" + search + "%") ))
    return query.order_by(User.rights.desc())\
                .paginate(page, per_page)


def get_count(school=None, is_apply=False, search=None):
    query = User.query
    if school:
        query = query.filter(User.school == school)
    if is_apply:
        query = query.filter(User.rights >= 8)
    else:
        query = query.filter(User.rights < 4) if school else query.filter(User.rights < 8)
    return query.count()


def modify_password(pwd_modify_form, current_user):
    user = get_by_id(pwd_modify_form.id.data)
    if not user:
        return u"不存在该用户"
    if not user.is_admin and user != current_user:
        return u"你没有权限修改密码"
    if pwd_modify_form.new_password.data != pwd_modify_form.new_password2.data:
        return u"两次输入的密码不同"
    user.password = pwd_modify_form.new_password.data
    user.save()
    return u"修改密码成功"


def get_statistic(user):
    statistic = dict()
    statistic['total_submit'] = user.submit.count()
    now = datetime.now()
    from datetime import timedelta
    permit_date = now - timedelta(days=now.weekday())
    permit_date = permit_date.replace(hour=0, minute=0, second=0)
    statistic['weekly_submit'] = user.submit.filter(Submit.submit_time > permit_date).count()
    return statistic
