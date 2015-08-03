from __init__ import *
from dao.dbHonor import Honor
import resource_server


def add_honor(honor_attr, user):
    try:
        honor = Honor()
        honor.title = honor_attr.title.data
        honor.introduce = honor_attr.introduce.data
        honor.contest_name = honor_attr.contest_name.data
        honor.contest_level = honor_attr.contest_level.data
        honor.acquire_time = honor_attr.acquire_time.data
        honor.resource = resource_server.get_by_id(honor_attr.resource_id.data)
        honor.user = user
        honor.save()
        return 'ok'
    except Exception:
        return 'failed'

def delete_honor(honor_id):
    try:
        Honor.query.filter(Honor.id==honor_id).delete()
        db.session.commit()
        return 'ok'
    except:
        return 'failed'

def modify_honor(honor_attr, user):
    try:
        honor = Honor.query.filter(Honor.id==honor_attr.id.data).first_or_404()
        honor.title = honor_attr.title.data
        honor.introduce = honor_attr.introduce.data
        honor.contest_name = honor_attr.contest_name.data
        honor.contest_level = honor_attr.contest_level.data
        honor.acquire_time = honor_attr.acquire_time.data
        honor.resource = resource_server.get_by_id(honor_attr.resource_id.data)
        honor.user = user
        honor.save()
        return 'ok'
    except:
        return 'failed'

def get_honor_list(offset=0, limit=10, filter_args=None):
    pass

def get_honor_count(offset=0, limit=10, filter_args=None):
    pass
