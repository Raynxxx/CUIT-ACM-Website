# coding=utf-8
from __init__ import *
from flask import current_app
from flask.ext.uploads import UploadSet, DEFAULTS, ARCHIVES, DOCUMENTS, TEXT, DATA, IMAGES, UploadNotAllowed
from dao.dbResource import Resource, ResourceLevel, ResourceUsage, ResourceType
from sqlalchemy import or_, and_
from sqlalchemy.exc import IntegrityError
import os, traceback

resource_uploader = UploadSet('resource', DEFAULTS + ARCHIVES, default_dest=lambda app: app.instance_root)


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
def save_file(file_attr, file_data, user, sub_folder):
    filename = ''
    try:
        filename = resource_uploader.save(file_data, folder=sub_folder,
                                          name=file_attr.name.data + '.')
        print filename
        rc = Resource()
        rc.filename = filename
        rc.name = file_attr.name.data
        rc.description = file_attr.description.data
        rc.user = user
        rc.level = file_attr.level.data if int(file_attr.level.data) in xrange(0, 3) else ResourceLevel.PRIVATE
        rc.usage = file_attr.usage.data if int(file_attr.usage.data) in xrange(0, 5) else ResourceUsage.OTHER_RES
        rc.upload_time = datetime.now()
        rc.type = get_type(rc.file_type)
        rc.save()
        return 'OK'
    except UploadNotAllowed:
        current_app.logger.error(traceback.format_exc())
        return 'your upload is not allowed'
    except IntegrityError:
        os.remove(resource_uploader.path(filename))
        db.session.rollback()
        current_app.logger.error(traceback.format_exc())
        return 'file name exist'
    except Exception:
        current_app.logger.error(traceback.format_exc())
        return 'filed to save your upload'


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
        current_app.logger.error(traceback.format_exc())
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
            return 'FAIL: No permission'
        path = resource_uploader.path(rc.filename)
        os.remove(path)
        rc.delete()
        return 'OK'
    except Exception:
        current_app.logger.error(traceback.format_exc())
        return 'FAIL'


def get_list(offset=0, limit=10, user=None, usage=None, type=None):
    if not user:
        query = Resource.query.filter(Resource.level==ResourceLevel.PUBLIC)
    elif user.is_admin:
        query = Resource.query
    elif user.is_coach:
        query = Resource.query.join(Resource.user)\
            .filter(or_(Resource.level<=ResourceLevel.SHARED, and_(User.school==user.school, User.rights < 4)))
    else:
        query = Resource.query.filter(or_(Resource.level<=ResourceLevel.SHARED, Resource.user==user),
                                      or_(Resource.usage==ResourceUsage.BLOG_RES,Resource.usage==ResourceUsage.OTHER_RES))
    if usage:
        query = query.filter(Resource.usage==usage)
    if type:
        query = query.filter(Resource.type==type)
    return query.order_by(Resource.upload_time.desc()).offset(offset).limit(limit).all()


def get_count(user=None, usage=None, type=None):
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
    return query.count()

def get_image_list(offset=0, limit=10, usage=ResourceUsage.NEWS_RES):
    query = Resource.query.filter(Resource.level==ResourceLevel.PUBLIC,
                                  Resource.type==ResourceType.IMAGES,
                                  Resource.usage==usage)
    return query.offset(offset).limit(limit).all()


def get_image_count(usage=ResourceUsage.NEWS_RES):
    query = Resource.query.filter(Resource.level==ResourceLevel.PUBLIC,
                                  Resource.type==ResourceType.IMAGES,
                                  Resource.usage==usage)
    return query.count()

def get_by_filename(filename):
    return Resource.query.filter(Resource.filename==filename).first_or_404()

def get_by_name(name):
    return Resource.query.filter(Resource.name==name).first_or_404()

def get_by_id(resource_id):
    return Resource.query.filter(Resource.id==resource_id).first_or_404()


def file_url(file):
    return resource_uploader.url(file.filename)


def file_size(file):
    try:
        return round(os.path.getsize(resource_uploader.path(file.filename)) / 1024.0, 2)
    except:
        return 0