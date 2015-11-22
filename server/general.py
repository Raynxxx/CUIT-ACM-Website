from __init__ import *
import sys
from dao.dbACCOUNT import AccountStatus
from dao.dbArticle import SolutionArticle
from sqlalchemy import or_
from flask import url_for
import time

#
# default limit set to 1024 ....
#
def get_rank_list(limit=1024):
    oj = ['bnu', 'hdu', 'poj', 'zoj', 'uva', 'cf', 'bc', 'vj']
    rank_list = []
    users = User.query.filter(User.active == 1, User.rights < 8)\
                .order_by(User.score.desc())\
                .limit(limit).all()
    for rank, user in enumerate(users):
        cur = {
            'rank': rank + 1,
            'user': '<a href="' + url_for('profile.index', username=user.username) +
                       '" target="_blank">' + user.name + '</a>',
        }
        for oj_name in oj:
            if oj_name in ['cf', 'bc']:
                cur[oj_name] = '0 (max 0)'
            else:
                cur[oj_name] = '0 / 0'
        if user.account:
            accounts = user.account.all()
            for account in accounts:
                problem_count = account.get_problem_count()
                if account.oj_name == 'cf':
                    cur[account.oj_name] = '<a href="http://codeforces.com/profile/' + account.nickname \
                                           + '"target="_blank">' + str(problem_count['rating']) + ' (max ' \
                                           + str(problem_count['max_rating']) + ')</a>'
                elif account.oj_name == 'bc':
                    cur[account.oj_name] = '<a href="http://bestcoder.hdu.edu.cn/rating.php?user=' + account.nickname \
                                           + '"target="_blank">' + str(problem_count['rating']) + ' (max ' \
                                           + str(problem_count['max_rating']) + ')</a>'
                else:
                    cur[account.oj_name] = str(problem_count['solved']) + ' / ' + str(problem_count['submitted'])
        rank_list.append(cur)
    return rank_list


def get_weekly_info(last_week, limit=100):
    oj = ['bnu', 'hdu', 'poj', 'zoj', 'uva', 'cf', 'bc']
    info_list = []
    if last_week:
        users = User.query.filter(User.active==1, User.rights < 8)\
                    .order_by(User.last_week_solved.desc(), User.score.desc())\
                    .limit(limit)
        for user in users:
            cur = {
                'sno': user.stu_id, 'name': user.name, 'username': user.username,
                'solved': user.last_week_solved, 'submitted': user.last_week_submit,
                'score': user.score
            }
            info_list.append(cur)
    else:
        users = User.query.filter(User.active==1, User.rights < 8)\
                    .order_by(User.current_week_solved.desc(), User.score.desc())\
                    .limit(limit)
        for user in users:
            cur = {
                'sno': user.stu_id, 'name': user.name, 'username': user.username,
                'solved': user.current_week_solved, 'submitted': user.current_week_submit,
                'score': user.score
            }
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


def update_all_account_status(user):
    if user.account:
        accounts = user.account.filter(Account.update_status==AccountStatus.NORMAL)\
                        .with_lockmode('update').all()
        for account in accounts:
            account.update_status = AccountStatus.WAIT_FOR_UPDATE
            account.save()
        db.session.commit()


def get_submit(oj_name, run_id):
    submit = Submit.query.filter_by(run_id=run_id, oj_name=oj_name).first()
    return submit

def get_submit_by_id(sid):
    submit = Submit.query.filter(Submit.id==sid).first()
    return submit


def related_article(submit, offset=0, limit=10):
    query = SolutionArticle.query.filter(SolutionArticle.problem_oj_name==submit.oj_name,
                                         SolutionArticle.problem_pid==submit.pro_id)
        #filter(or_(Submit.result == 'OK', Submit.result == 'Accepted')).all()
    return query.offset(offset).limit(limit).all()


def related_article_count(submit):
    query = SolutionArticle.query.filter(SolutionArticle.problem_oj_name==submit.oj_name,
                                         SolutionArticle.problem_pid==submit.pro_id)
        #filter(or_(Submit.result == 'OK', Submit.result == 'Accepted')).all()
    return query.count()


def get_sys_info():
    sys_info = dict()
    sys_info['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    import user_server
    sys_info['user_count'] = user_server.get_count()
    sys_info['apply_count'] = user_server.get_count(isApply=True)
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    sys_info['daily_submit'] = Submit.query.filter(Submit.submit_time > today).count()
    sys_info['total_submit'] = Submit.query.count()
    sys_info['news_count'] = News.query.count()
    sys_info['honor_count'] = Honor.query.count()
    return sys_info
