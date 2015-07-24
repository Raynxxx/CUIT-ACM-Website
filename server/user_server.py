# coding=utf-8
from __init__ import *
from config import OJ_MAP, SCHOOL_MAP


def create_user(user_form, user_rights):
    has_user = User.query.filter_by(username=user_form.username.data).first()
    if has_user:
        return "该用户名已经存在"
    new_user = User(username = user_form.username.data,
                name = user_form.name.data,
                password = user_form.password.data,
                school = SCHOOL_MAP[user_form.school.data],
                gender = True if user_form.gender.data == '1' else False,
                email = user_form.email.data)
    new_user.rights = user_rights
    new_user.stu_id = user_form.stu_id.data
    new_user.phone = user_form.phone.data
    new_user.save()
    return 'OK'


def update_user(user_form, user_rights=None, for_self = False):
    has_user = User.query.filter_by(id = user_form.id.data).first()
    if not has_user:
        return u"该用户不存在"
    has_user.name = user_form.name.data
    has_user.school = user_form.school.data
    has_user.gender = True if user_form.gender.data == '1' else False
    has_user.email = user_form.email.data
    if not for_self:
        has_user.rights = user_rights
    has_user.stu_id = user_form.stu_id.data
    has_user.phone = user_form.phone.data
    has_user.remark = user_form.motto.data
    has_user.situation = user_form.situation.data
    has_user.active = int(user_form.active.data)
    has_user.save()
    return 'OK'


def delete_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.delete()


def get_by_id(user_id):
    return  User.query.filter_by(id=user_id).first()


def get_by_username_or_404(username):
    return User.query.filter_by(username=username).first_or_404()


def get_by_username(username):
    return User.query.filter_by(username=username).first()


def get_list(offset=0, limit=20, is_admin=True, school=None):
    if is_admin:
        users = User.query.offset(offset).limit(limit).all()
    else:
        all_users = User.query.filter(User.school==school).offset(offset).limit(limit).all()
        users = list()
        for user in all_users:
            users.append(user) if not user.is_admin else None
    return users


def get_count(is_admin=True, school=None):
    if is_admin:
        count = User.query.count()
    else:
        all_users = User.query.filter(User.school==school).all()
        count = 0
        for user in all_users:
            count = count + 1 if not user.is_admin else count
    return count


def modify_password(user, pwd_form):
    user = get_by_username(pwd_form.username.data)
    if not user:
        return u"不存在该用户"
    if not user.is_admin and user != user:
        return u"你没有权限修改密码"
    if pwd_form.password.data != pwd_form.verifypassword.data:
        return u"两次输入的密码不同"
    user.password = pwd_form.password.data
    user.save()
    return u"修改密码成功"


def get_statistic(user):
    statistic = dict()
    statistic['total_submit'] = user.submit.count()
    now = datetime.datetime.now()
    permit_date = now - datetime.timedelta(days=now.weekday())
    permit_date = permit_date.replace(hour=0, minute=0, second=0)
    statistic['weekly_submit'] = user.submit.filter(Submit.submit_time > permit_date).count()
    return statistic


def get_account_info(user):
    have = []
    not_have = []
    if user.account:
        accounts = user.account.all()
        for account in accounts:
            have.append(account.oj_name)
    for oj_name in OJ_MAP:
        if oj_name not in have:
            not_have.append(oj_name)
    return { 'have': have, 'not_have': not_have }


def get_general_info(user, oj_name):
    if not user.account:
        return None
    account = user.account.filter_by(oj_name=oj_name).first()
    if account:
        ret = account.get_problem_count()
        ret['last_update_time'] = account.last_update_time
        return ret
    return None


