from __init__ import *
import sys
from dao.dbACCOUNT import AccountStatus
import time
from sqlalchemy import or_


def get_info_list(lim=100):
    oj = ['bnu', 'hdu', 'poj', 'zoj', 'uva', 'cf', 'bc', 'vj']
    info_list = []
    users = User.query.filter(User.active==1).order_by(User.score.desc()).limit(lim)
    rank = 1
    for user in users:
        cur = {'sno': user.stu_id, 'name': user.name, 'username': user.username, 'score': user.score, 'rank': rank}
        for oj_name in oj:
            if oj_name in ['cf', 'bc']:
                cur[oj_name] = {'rating': 0, 'max_rating': 0}
            else:
                cur[oj_name] = {'solved': 0, 'submitted': 0}
        if user.account:
            accounts = user.account.all()
            for account in accounts:
                cur[account.oj_name] = account.get_problem_count()
                if account.oj_name in ['cf', 'bc']:
                    cur[account.oj_name + '_username'] = account.nickname
        info_list.append(cur)
        rank += 1
    return info_list


def get_weekly_info(lastweek, lim=100):
    oj = ['bnu', 'hdu', 'poj', 'zoj', 'uva', 'cf', 'bc']
    info_list = []
    if lastweek:
        users = User.query.filter(User.active==1).order_by(User.last_week_solved.desc()).limit(lim)
        for user in users:
            cur = {'sno': user.stu_id, 'name': user.name, 'username': user.username, 'solved': user.last_week_solved,
                   'submitted': user.last_week_submit}
            info_list.append(cur)
    else:
        users = User.query.filter(User.active==1).order_by(User.current_week_solved.desc()).limit(lim)
        for user in users:
            cur = {'sno': user.stu_id, 'name': user.name, 'username': user.username, 'solved': user.current_week_solved,
                   'submitted': user.current_week_submit}
            info_list.append(cur)
    rank = 1
    for info in info_list:
        info['rank'] = rank
        rank += 1
    return info_list



def check_update_status(user):
    update_status = False
    if user.account:
        accounts = user.account.all()
        for account in accounts:
            if account and account.update_status != 0:
                update_status = True
    return update_status


def update_user_status(user):
    if user.account:
        accounts = user.account.all()
        for account in accounts:
            if account and account.update_status != AccountStatus.UPDATING:
                account.update_status = AccountStatus.WAIT_FOR_UPDATE
                account.save()


def recrawl_status(oj_name, run_id):
    status = Submit.query.filter(Submit.oj_name == oj_name, Submit.run_id == run_id).first()
    if status:
        status.update_status = 1
        status.save()


def get_submit(oj_name, run_id):
    submit = Submit.query.filter_by(run_id=run_id, oj_name=oj_name).first()
    return submit


def get_sys_info():
    sys_info = dict()
    sys_info['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sys_info['user_count'] = User.query.count()
    permit_date = datetime.datetime.now() - datetime.timedelta(days=1)
    sys_info['daily_submit'] = len(Submit.query.filter(Submit.submit_time > permit_date).all())
    sys_info['total_submit'] = Submit.query.count()
    return sys_info
