# coding=utf-8
from __init__ import *

def add_account(user, param):
    account = Account(param.oj_name.data, param.nickname.data, param.password.data, user)
    account.save()

def delete_account(user, oj_name):
    account = Account.query.filter(Account.user == user, Account.oj_name == oj_name).first()
    if account:
        Submit.query.filter(Submit.user == user, Submit.oj_name == oj_name).delete()
        account.user.update_score()
        db.session.delete(account)
        db.session.commit()

def modify_account(origin, param):
    Submit.query.filter(Submit.user == origin.user, Submit.oj_name == origin.oj_name).delete()
    db.session.commit()
    origin.oj_name = param.oj_name.data
    origin.nickname = param.nickname.data
    origin.password = param.password.data
    origin.update_status = 1
    origin.save()

def get_account_info(user):
    accounts = user.account
    data = []
    for account in accounts:
        account_info = {
            'account_name': account.nickname,
            'oj_name': account.oj_name,
            'status': 'UNKOWN',
        }
        data.append(account_info)
    return data