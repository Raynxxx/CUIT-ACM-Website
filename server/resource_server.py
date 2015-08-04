from __init__ import *
from flask.ext.uploads import UploadSet, DEFAULTS, ARCHIVES, DOCUMENTS, TEXT, DATA, IMAGES, UploadNotAllowed
import datetime, os
from dao.dbResource import Resource, ResourceLevel, ResourceUsage, ResourceType
from sqlalchemy import or_, and_

resource = UploadSet('resource', DEFAULTS + ARCHIVES, default_dest=lambda app: app.instance_root)


def get_type(file_type):
    if file_type in TEXT:
        return ResourceType.TEXT
    elif file_type in DOCUMENTS:
        return ResourceType.DOCUMENTS
    elif file_type in DATA:
        return ResourceType.DATA
    elif file_type in IMAGES:
        return ResourceType.IMAGES
    elif file_type in ARCHIVES:
        return ResourceType.ARCHIVES
    else:
        return ResourceType.OTHER


#
# @brief: save one file to the configured path
# @arg1: file_attr (file_upload_form)
# @arg2: file_data (file)
# return 'ok' if ok else the error msg
#
def save_file(file_attr, file_data, user):
    try:
        filename = resource.save(file_data, name=file_attr.name.data + '.')
        rc = Resource()
        rc.filename = filename
        rc.name = file_attr.name.data
        rc.description = file_attr.description.data
        rc.user = user
        rc.level = file_attr.level.data if int(file_attr.level.data) in xrange(0, 3) else ResourceLevel.PRIVATE
        rc.usage = file_attr.usage.data if int(file_attr.usage.data) in xrange(0, 5) else ResourceUsage.OTHER_RES
        rc.upload_time = datetime.datetime.now()
        rc.type = get_type(rc.file_type)
        rc.save()
        return 'ok'
    except UploadNotAllowed:
        return 'your upload is not allowed'
    except Exception, e:
        return 'filed to save you upload'


def modify_file(file_attr, user):
    try:
        rc = Resource.query.filter(Resource.id==file_attr.id.data).first_or_404()
        if rc.user != user and not user.is_admin and not user.is_coach_of(rc.user):
            return 'failed, no permission'
        rc.name = file_attr.name.data
        rc.description = file_attr.description.data
        rc.level = file_attr.level.data if int(file_attr.level.data) in xrange(0, 3) else ResourceLevel.PRIVATE
        rc.usage = file_attr.usage.data if int(file_attr.usage.data) in xrange(0, 5) else ResourceUsage.OTHER_RES
        rc.save()
        return 'ok'
    except Exception:
        return 'failed'


#
# @brief: delete one file
# @arg1: resource_id (the resource id in the db)
# return 'ok' if ok else the error msg
#
def delete_file(resource_id, user):
    try:
        rc = Resource.query.filter(Resource.id==resource_id).first_or_404()
        if rc.user != user and not user.is_admin and not user.is_coach_of(rc.user):
            return 'failed, no permission'
        path = resource.path(rc.filename)
        os.remove(path)
        rc.delete()
        return 'ok'
    except Exception:
        return 'failed'


def get_list(offset=0, limit=10, user=None, usage=None, type=None, level=None):
    if not user:
        query = Resource.query.filter(Resource.level==ResourceLevel.PUBLIC)
    elif user.is_admin:
        query = Resource.query
    elif user.is_coach:
        query = Resource.query.join(Resource.user)\
            .filter(or_(Resource.level<=ResourceLevel.SHARED, and_(User.school==user.school, User.rights < 4)))
    else:
        query = Resource.query.filter(or_(Resource.level<=ResourceLevel.SHARED, Resource.user==user))
    if usage:
        query = query.filter(Resource.usage==usage)
    if type:
        query = query.filter(Resource.type==type)
    if level:
        query = query.filter(Resource.level==level)
    return query.offset(offset).limit(limit).all()

def get_count(user=None, usage=None, type=None, level=None):
    if not user:
        query = Resource.query.filter(Resource.level==ResourceLevel.PUBLIC)
    elif user.is_admin:
        query = Resource.query
    elif user.is_coach:
        query = Resource.query.join(Resource.user)\
            .filter(or_(Resource.level<=ResourceLevel.SHARED, and_(User.school==user.school, User.rights < 4)))
    else:
        query = Resource.query.filter(or_(Resource.level<=ResourceLevel.SHARED, Resource.user==user))
    if usage:
        query =  query.filter(Resource.usage==usage)
    if type:
        query = query.filter(Resource.type==type)
    if level:
        query = query.filter(Resource.level==level)
    return query.count()

def get_by_name(filename):
    return Resource.query.filter(Resource.filename==filename).first_or_404()

def get_by_id(resource_id):
    return Resource.query.filter(Resource.id==resource_id).first_or_404()


def file_url(file):
    return resource.url(file.filename)


def file_size(file):
    try:
        return round(os.path.getsize(resource.path(file.filename)) / 1024.0, 2)
    except:
        return 0