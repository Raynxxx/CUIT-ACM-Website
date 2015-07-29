from __init__ import *
from flask.ext.uploads import (UploadSet, DEFAULTS, ARCHIVES, UploadNotAllowed)
import datetime
import os
from dao.dbResource import Resource

resource = UploadSet('resource', DEFAULTS + ARCHIVES, default_dest=lambda app: app.instance_root)


#
# @brief: save one file to the configured path
# @arg1: file_attr (file_upload_form)
# @arg2: file_data (file)
# return 'ok' if ok else the error msg
#
def save_file(file_attr, file_data, user):
    try:
        filename = resource.save(file_data,name=file_attr.name.data+'.')
        rc = Resource()
        rc.name = filename
        rc.description = file_attr.description.data
        rc.user = user
        rc.upload_time = datetime.datetime.now()
        rc.save()
        return 'ok'
    except UploadNotAllowed:
        return 'you upload is not allowed'
    except Exception, e:
        print(e.message)
        return 'filed to save you upload'

#
# @brief: delete one file
# @arg1: resource_id (the resource id in the db)
# return 'ok' if ok else the error msg
#
def delete_file(resource_id):
    try:
        rc = Resource.query.filter(Resource.id==resource_id).first_or_404()
        path = resource.path(rc.name)
        os.remove(path)
        rc.delete()
        return 'ok'
    except Exception:
        return 'failed'

def get_list(offset=0, limit=10, coach=None):
    if coach :
        return Resource.query.filter(Resource.user==coach).offset(offset).limit(limit).all()
    else :
        return Resource.query.offset(offset).limit(limit).all()

def get_count(coach=None):
    if coach :
        return Resource.query.filter(Resource.user==coach).count()
    else :
        return Resource.query.count()

def url(filename):
    return resource.url(filename)