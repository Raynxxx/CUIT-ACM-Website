# coding=utf-8
from __init__ import *
from config import OJ_MAP
from dao.dbACCOUNT import AccountStatus


class AccountUpdatingException(BaseException):
    pass

class AccountExistException(BaseException):
    pass


def add_account(user, param):
    if Account.query.filter(Account.oj_name==param.oj_name.data, Account.nickname==param.nickname.data).count():
        raise AccountExistException(u'账号已被另一个学生添加')
    account = Account(param.oj_name.data, param.nickname.data, param.password.data, user)
    account.save()


def delete_account_by_id(user, account_id):
    account = Account.query.filter_by(id = account_id).with_lockmode('update').first()
    if account:
        if account.update_status == AccountStatus.UPDATING:
            raise AccountUpdatingException(u'Account is updating')
        Submit.query.filter(Submit.user == user, Submit.oj_name == account.oj_name).delete()
        db.session.commit()
        account_user_id = account.user.id
        account.delete()
        account_user = User.query.filter(User.id==account_user_id).with_lockmode('update').first()
        account_user.update_score()
        account_user.save()
    else:
        db.session.commit()


def delete_account(user, oj_name):
    account = Account.query.filter(Account.user == user, Account.oj_name == oj_name).with_lockmode('update').first()
    if account:
        if account.update_status == AccountStatus.UPDATING:
            raise AccountUpdatingException('Account is updating')
        Submit.query.filter(Submit.user == user, Submit.oj_name == oj_name).delete()
        db.session.commit()
        account_user_id = account.user.id
        account.delete()
        account_user = User.query.filter(User.id==account_user_id).with_lockmode('update').first()
        account_user.update_score()
        account_user.save()
    else:
        db.session.commit()


def update_account_by_id(account_id):
    account = Account.query.filter(Account.id == account_id, Account.update_status==AccountStatus.NORMAL)\
        .with_lockmode('update').first()
    if not account:
        db.session.commit()
    else:
        account.update_status = AccountStatus.WAIT_FOR_UPDATE
        account.save()

def modify_account(origin, param):
    if origin.update_status == AccountStatus.UPDATING:
        raise AccountUpdatingException('Account is updating')
    Submit.query.filter(Submit.user == origin.user, Submit.oj_name == origin.oj_name).delete()
    db.session.commit()
    account = Account(param.oj_name.data, param.nickname.data, param.password.data, origin.user)
    origin.delete()
    account.save()


def get_account_info_list(user):
    accounts = user.account
    status_mapper = {
        AccountStatus.NORMAL:           u'正常',
        AccountStatus.NOT_INIT:         u'未初始化',
        AccountStatus.WAIT_FOR_UPDATE:  u'等待更新',
        AccountStatus.UPDATING:         u'正在更新',
        AccountStatus.UPDATE_ERROR:     u'更新失败'
    }
    data = []
    for account in accounts:
        account_info = account.get_problem_count()
        account_info['id'] = account.id
        account_info['account_name'] = account.nickname
        account_info['oj_name'] = OJ_MAP[account.oj_name]
        account_info['status'] = status_mapper[int(account.update_status)]
        account_info['last_update_time'] = account.last_update_time
        data.append(account_info)
    return data