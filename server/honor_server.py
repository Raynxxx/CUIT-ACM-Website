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
        honor.title = honor_attr.title.data
        honor.md_introduce = honor_attr.introduce.data
        honor.contest_name = honor_attr.contest_name.data
        honor.contest_level = honor_attr.contest_level.data
        honor.acquire_time = honor_attr.acquire_time.data
        honor.type = honor_attr.type.data
        honor.resources = honor_resource
        honor.users = user_list
        honor.save()
        return 'ok'
    except UserNotExist, e:
        return e.message
    except Exception:
        return 'failed'

def delete_honor(honor_id):
    try:
        Honor.query.filter(Honor.id==honor_id).delete()
        db.session.commit()
        return 'ok'
    except:
        return 'failed'

def modify_honor(honor_attr):
    try:
        honor = Honor.query.filter(Honor.id==honor_attr.id.data).first_or_404()
        honor.title = honor_attr.title.data
        user_list = get_users(honor_attr.users.data)
        honor.md_introduce = honor_attr.introduce.data
        honor.contest_name = honor_attr.contest_name.data
        honor.contest_level = honor_attr.contest_level.data
        honor.acquire_time = honor_attr.acquire_time.data
        honor.users = user_list
        honor.save()
        return 'ok'
    except UserNotExist, e:
        return e.message
    except Exception, e:
        return 'failed'

def get_honor_list(offset=0, limit=10):
        return Honor.query.offset(offset).limit(limit).all()

def get_honor_wall(offset=0, limit=10, query_type=None, keyword=''):
    if query_type == 'user':
        user = User.query.filter(User.name==keyword).first()
        if user:
            return user.honors.order_by(Honor.acquire_time.desc()).offset(offset).limit(limit).all()
        else:
            return list()
    elif query_type == 'time':
        year = datetime.datetime(keyword,0,0)
        return Honor.query.filter(Honor.acquire_time.between(year,year + datetime.timedelta(days=365))).\
            order_by(Honor.acquire_time.desc()).offset(offset).limit(limit).all()
    elif query_type == 'level':
        return Honor.query.filter(Honor.contest_level==keyword).\
            order_by(Honor.acquire_time.desc()).offset(offset).limit(limit).all()
    elif query_type == 'contest':
        return Honor.query.filter(Honor.contest_name.like('%'+keyword+'%')).\
            order_by(Honor.acquire_time.desc()).offset(offset).limit(limit).all()
    else:
        return Honor.query.order_by(Honor.acquire_time.desc()).offset(offset).limit(limit).all()


def get_honor_count(offset=0, limit=10):
    return Honor.query.count()

def get_by_id(sid):
    return Honor.query.filter(Honor.id == sid).first_or_404()
