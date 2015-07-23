# coding=utf-8
from __init__ import *
from dao.dbACCOUNT import AccountStatus


class AccountUpdatingException(BaseException):
    pass

def add_account(user, param):
    account = Account(param.oj_name.data, param.nickname.data, param.password.data, user)
    account.save()

def delete_account(user, oj_name):
    account = Account.query.filter(Account.user == user, Account.oj_name == oj_name).first()
    if account:
        if account.update_status == AccountStatus.UPDATING:
            raise AccountUpdatingException('Account is updating')
        Submit.query.filter(Submit.user == user, Submit.oj_name == oj_name).delete()
        db.session.commit()
        account.user.update_score()
        account.delete()

def modify_account(origin, param):
    if origin.update_status == AccountStatus.UPDATING:
        raise AccountUpdatingException('Account is updating')
    Submit.query.filter(Submit.user == origin.user, Submit.oj_name == origin.oj_name).delete()
    db.session.commit()
    account = Account(param.oj_name.data, param.nickname.data, param.password.data, origin.user)
    origin.delete()
    account.save()

def get_account_info(user):
    accounts = user.account
    status_mapper = {AccountStatus.NORMAL:u'正常',AccountStatus.NOT_INIT:u'未初始化', AccountStatus.UPDATING:u'正在更新', AccountStatus.UPDATE_ERROR:u'更新失败'}
    data = []
    for account in accounts:
        account_info = {
            'account_name': account.nickname,
            'oj_name': account.oj_name,
            'status': status_mapper[account.update_status],
        }
        data.append(account_info)
    return data