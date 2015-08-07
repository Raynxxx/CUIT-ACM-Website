# coding=utf-8
from __init__ import *
from dao.dbHonor import Honor
from dao.dbBase import User
import resource_server


class UserNotExist(BaseException):
    pass


def get_users(data):
    user_list = []
    for name in data:
        if name == '':
            continue
        user = User.query.filter(User.username == name).first()
        if not user:
            raise UserNotExist(u'user not exist')
        else:
            user_list.append(user)
    return user_list


def add_honor(honor_attr, honor_resource):
    try:
        honor = Honor()
        user_list = get_users(honor_attr.users.data)
        honor.contest_name = honor_attr.contest_name.data
        honor.contest_level = honor_attr.contest_level.data
        honor.acquire_time = honor_attr.acquire_time.data
        honor.type = honor_attr.type.data
        honor.md_introduce = honor_attr.introduce.data
        honor.resources = honor_resource
        honor.users = user_list
        honor.save()
        return u'添加成功'
    except UserNotExist, e:
        return e.message
    except Exception:
        return u'添加失败'


def delete_honor(honor_id):
    try:
        Honor.query.filter(Honor.id==honor_id).delete()
        db.session.commit()
        return u'删除成功'
    except:
        return u'删除失败'


def modify_honor(honor_attr):
    try:
        honor = Honor.query.filter(Honor.id==honor_attr.id.data).first_or_404()
        user_list = get_users(honor_attr.users.data)
        honor.contest_name = honor_attr.contest_name.data
        honor.contest_level = honor_attr.contest_level.data
        honor.acquire_time = honor_attr.acquire_time.data
        honor.md_introduce = honor_attr.introduce.data
        honor.users = user_list
        honor.save()
        return u'修改成功'
    except UserNotExist, e:
        return e.message
    except Exception, e:
        return u'修改失败'


def get_honor_list(offset=0, limit=10):
        return Honor.query.offset(offset).limit(limit).all()


def get_honor_wall(offset=0, limit=10, query_type=None, keyword=''):
    if query_type == 'user' and keyword != '':
        user = User.query.filter(User.name==keyword).first()
        return user.honors.order_by(Honor.acquire_time.desc())\
            .offset(offset).limit(limit).all() if user else []
    elif query_type == 'time' and keyword != '':
        try:
            year = int(keyword)
        except:
            year = datetime.date.min.year
        year_start = datetime.datetime(year, 1, 1)
        year_end = datetime.datetime(year, 12, 31)
        return Honor.query\
            .filter(Honor.acquire_time.between(year_start, year_end)).\
            order_by(Honor.acquire_time.desc())\
            .offset(offset).limit(limit).all()
    elif query_type == 'level' and keyword != '':
        return Honor.query\
            .filter(Honor.contest_level==keyword).\
            order_by(Honor.acquire_time.desc())\
            .offset(offset).limit(limit).all()
    elif query_type == 'contest_name' and keyword != '':
        return Honor.query\
            .filter(Honor.contest_name.like('%' + keyword + '%')).\
            order_by(Honor.acquire_time.desc())\
            .offset(offset).limit(limit).all()
    else:
        return Honor.query\
            .order_by(Honor.acquire_time.desc())\
            .offset(offset).limit(limit).all()


def get_honor_wall_by_year(offset=0, limit=10, query_type=None, keyword=''):
    honor_list = get_honor_wall(offset, limit, query_type, keyword)
    honor_wall = dict()
    for honor in honor_list:
        year = honor.acquire_time.year
        if year not in honor_wall:
            honor_wall[year] = []
        honor_wall[year].append(honor)
    return honor_wall


def get_honor_count(query_type=None, keyword=''):
    if query_type == 'user' and keyword != '':
        user = User.query.filter(User.name==keyword).first()
        return user.honors\
            .count() if user else 0
    elif query_type == 'time' and keyword != '':
        year = datetime.datetime(int(keyword), 0, 0)
        next_year = datetime.datetime(int(keyword), 0, 0)
        return Honor.query\
            .filter(Honor.acquire_time.between(year,year + next_year))\
            .count()
    elif query_type == 'level' and keyword != '':
        return Honor.query\
            .filter(Honor.contest_level==keyword)\
            .count()
    elif query_type == 'contest_name' and keyword != '':
        return Honor.query\
            .filter(Honor.contest_name.like('%' + keyword + '%'))\
            .count()
    else:
        return Honor.query.count()


def get_by_id(sid):
    return Honor.query.filter(Honor.id == sid).first_or_404()
