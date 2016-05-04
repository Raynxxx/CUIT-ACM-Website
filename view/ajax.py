# coding=utf-8
import os
from __init__ import *
import traceback, cStringIO, re
from flask import current_app
from werkzeug.datastructures import FileStorage
from server import user_server, article_server, status_server, form, \
    account_server, news_server, resource_server
from server import general, honor_server
from dao.dbACCOUNT import Account
from dao import dbCompetition, dbPlayer
from util import json, CJsonEncoder
from flask.globals import _app_ctx_stack
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from server.account_server import AccountUpdatingException, AccountExistException
from util import function

#
# @blueprint: ajax
# @created: 2015/06/22
# @author: Z2Y
#
ajax = blueprints.Blueprint('ajax', __name__)


#
# @brief: json for recent contest
# @route: /ajax/contest.json
# @allowed user: public
#
@ajax.route("/ajax/contest.json", methods=['GET'])
def recent_contests():
    import json
    json_file = open(RECENT_CONTEST_JSON, 'r').read()
    json_contests = json.JSONDecoder().decode(json_file)
    contests = []
    for contest in json_contests:
        name, link = contest['name'], contest['link']
        new_contest = {
            'oj': contest['oj'],
            'name': '<a href="' + link + '" class="contest-name" title="' + name + '">' + name + '</a>',
            'start_time': contest['start_time'],
            'access': contest['access'],
        }
        contests.append(new_contest)
    return json.dumps({ 'data': contests })


#
# @brief: ajax rank list
# @route: /ajax/rank_list
# @allowed user: student and coach
#
@ajax.route('/ajax/main_rank_table')
def main_rank_table():
    main_rank_list = general.get_rank_list()
    return json.dumps({ 'data': main_rank_list })



#
# @brief: ajax html for one user item
# @allowed user: admin and coach
#
@login_required
def get_user_list_item(user):
    return render_template('ajax/user_list_item.html',
                           user = user,
                           school_mapper = SCHOOL_MAP,
                           college_mapper = SCHOOL_COLLEGE_MAP)

#
# @brief: ajax user list
# @route: /ajax/user_list
# @allowed user: admin and coach
#
@ajax.route('/ajax/user_list', methods=["GET", "POST"])
@login_required
def get_users():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', None)
    per_page = USER_MANAGE_PER_PAGE
    pagination = None
    if current_user.is_admin:
        pagination = user_server.get_list_pageable(page, per_page, search=search)
    elif current_user.is_coach:
        pagination = user_server.get_list_pageable(page, per_page, search=search,
                                                   school=current_user.school)
    page_list = list(pagination.iter_pages(left_current=1, right_current=2))
    return jsonify(items=[get_user_list_item(user) for user in pagination.items],
                   prev_num=pagination.prev_num,
                   next_num=pagination.next_num,
                   page_list=page_list,
                   page=pagination.page,
                   pages=pagination.pages)


#
# @brief: add user
# @route: /ajax/create_user
# @accepted methods: [post]
# @allowed user: admin and coach
# @ajax return: 用户是否添加成功
#
@ajax.route('/ajax/create_user', methods=["POST"])
@login_required
def create_user():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    reg_form = form.RegisterForm()
    if reg_form.validate_on_submit():
        try:
            rights_list = request.form.getlist('rights')
            rights = 0
            for item in rights_list:
                rights = rights | int(item)
            ret = user_server.create_user(reg_form, rights)
            if ret == 'OK':
                return u"添加用户成功"
            return u"添加用户失败: " + ret
        except Exception, e:
            current_app.logger.error(traceback.format_exc())
            return u"添加用户失败: " + e.message
    else:
        #print reg_form.errors
        return u"添加用户失败: 表单填写有误"


#
# @brief: add many users
# @route: /ajax/create_users
# @accepted methods: [post]
# @allowed user: admin and coach
# @ajax return: 用户添加成功的数量
#
@ajax.route('/ajax/create_users', methods=["POST"])
@login_required
def create_users():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    reg_form = form.MultiRegisterForm()
    if reg_form.validate_on_submit():
        try:
            ret = user_server.create_many_users(reg_form, current_user)
            return ret
        except Exception, e:
            current_app.logger.error(traceback.format_exc())
            return u"添加用户失败: " + e.message
    else:
        #print reg_form.errors
        return u"添加用户失败: 表单填写有误"


#
# @brief: check apply user
# @route: /ajax/check_apply
# @accepted methods: [post]
# @allowed user: admin and coach
# @ajax return: 操作结果
#
@ajax.route("/ajax/check_apply", methods= ['POST'])
@login_required
def check_apply():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    try:
        apply_id = request.form.get('uid')
        user = user_server.get_by_id(apply_id)
        opt = request.form.get('opt')
        ret = user_server.update_apply(apply_id, opt)
        if ret == 'OK':
            function.reply_of_apply(mail, user.serialize, _app_ctx_stack.top, opt)
        return ret
    except Exception:
        current_app.logger.error(traceback.format_exc())
        return u'操作失败'


#
# @brief: edit user
# @route: /ajax/edit_user
# @accepted methods: [post]
# @allowed user: admin and coach
#
@ajax.route('/ajax/edit_user', methods=["POST"])
@login_required
def edit_user():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    user_modify_form = form.UserModifyForm()
    if user_modify_form.validate_on_submit():
        try:
            rights_list = request.form.getlist('rights')
            rights = 0
            for item in rights_list:
                rights = rights | int(item)
            ret = user_server.update_user(user_modify_form, rights)
            if ret == 'OK':
                return u"修改用户成功"
            return u'修改用户失败: ' + ret
        except Exception, e:
            current_app.logger.error(traceback.format_exc())
            return u"修改用户失败: " + e.message
    else:
        #print user_modify_form.errors
        return u"修改用户失败: 表单填写有误"


#
# @brief: edit user for self
# @route: /ajax/edit_user_self
# @accepted methods: [post]
# @allowed user: all
#
@ajax.route('/ajax/edit_user_self', methods=["POST"])
@login_required
def edit_user_self():
    user_modify_form = form.UserModifyForm()
    if user_modify_form.validate_on_submit():
        try:
            ret = user_server.update_user(user_modify_form, for_self=True)
            if ret == 'OK':
                return u"修改用户成功"
            return u'修改用户失败: ' + ret
        except Exception, e:
            current_app.logger.error(traceback.format_exc())
            return u"修改用户失败: " + e.message
    else:
        #print user_modify_form.errors
        return u"修改用户失败: 表单填写有误"


#
# @brief: modify password
# @route: /ajax/modify_password
# @accepted methods: [post]
# @allowed user: all
# @ajax return: 密码是否修改成功 => string
#
@ajax.route('/ajax/modify_password', methods=['POST'])
@login_required
def modify_password():
    pwd_modify_form = form.PasswordModifyForm()
    if pwd_modify_form.validate_on_submit():
        if not current_user.verify_password(pwd_modify_form.password.data):
            return u"当前密码输入错误"
        return user_server.modify_password(pwd_modify_form, current_user)
    return u"修改密码失败"


#
# @brief: delete user
# @route: /ajax/delete_user
# @accepted methods: [post]
# @allowed user: admin and coach
#
@ajax.route('/ajax/delete_user', methods=["POST"])
@login_required
def delete_user():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    try:
        id = request.form.get('user_id')
        user_server.delete_by_id(id)
        return u"OK"
    except Exception, e:
        current_app.logger.error(traceback.format_exc())
        return u"FAIL"


#
# @brief: ajax html for one user item
# @allowed user: administrator
#
@login_required
def get_news_list_item(news):
    return render_template('ajax/news_list_item.html', news=news)


#
# @brief: ajax news list
# @route: /ajax/news_list
# @allowed user: administrator
#
@ajax.route('/ajax/news_list', methods=['GET', 'POST'])
@login_required
def get_news_list():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', None)
    per_page = NEWS_MANAGE_PER_PAGE
    pagination = news_server.get_list_pageable(page, per_page, show_draft=True, search=search)
    page_list = list(pagination.iter_pages(left_current=1, right_current=2))
    return jsonify(items=[get_news_list_item(news) for news in pagination.items],
                   prev_num=pagination.prev_num,
                   next_num=pagination.next_num,
                   page_list=page_list,
                   page=pagination.page,
                   pages=pagination.pages)


#
# @brief: delete news
# @route: /ajax/delete_news
# @accepted methods: [post]
# @allowed user: admin and coach
#
@ajax.route("/ajax/delete_news", methods = ['POST'])
@login_required
def delete_news():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    try:
        news_id = request.form.get('news_id')
        news_server.delete_by_id(news_id)
        return u'OK'
    except Exception, e:
        current_app.logger.error(traceback.format_exc())
        return u'FAIL'

#
# @brief: post news
# @route: /ajax/post_news
# @accepted methods: [post]
# @allowed user: admin and coach
#
@ajax.route('/ajax/post_news', methods=['POST'])
@login_required
def post_news():
    if not current_user.is_admin and not current_user.is_coach:
        return u"没有权限"
    news_form = form.NewsForm()
    if news_form.validate_on_submit():
        try:
            is_draft = int(request.args['draft'])
            news_server.post(news_form, current_user, is_draft)
            return u"发表成功!"
        except IntegrityError:
            current_app.logger.error(traceback.format_exc())
            return u"发表新闻失败: 固定链接已存在"
        except Exception, e:
            current_app.logger.error(traceback.format_exc())
            return u"发表新闻失败: " + e.message
    else:
        return u"发表新闻失败,请检查内容"



#
# @brief: ajax html for one account item
# @allowed user: self, admin and coach
#
@login_required
def get_account_item(account, user):
    return render_template('ajax/account_info_item.html',
                           account = account,
                           user = user, str = str)


#
# @brief: add or modify account
# @route: /ajax/account_manager
# @accepted methods: [post]
# @allowed user: administrator or the user
#
@ajax.route('/ajax/account_info_list', methods=['POST', 'GET'])
@login_required
def account_info_list():
    try:
        profile_user = user_server.get_by_username_or_404(request.args['username'])
    except:
        profile_user = current_user
    account_info_list = account_server.get_account_info_list(profile_user)
    return jsonify(account_list = [get_account_item(account_info, profile_user) for account_info in account_info_list],
                   length = len(account_info_list))


#
# @brief: update the statistics info of account
# @route: /ajax/update_account
# @accepted methods: [post]
# @allowed user: admin, coach or the user
#
@ajax.route('/ajax/update_account', methods=['POST'])
@login_required
def update_account():
    try:
        profile_user = user_server.get_by_id(request.form.get('user_id'))
    except:
        profile_user = current_user
    if profile_user != current_user and\
            (not current_user.is_admin and not current_user.is_coach_of(profile_user)):
        return u"没有权限"
    try:
        account_id = request.form.get('account_id')
        account_server.update_account_by_id(account_id)
        return u"ok"
    except AccountUpdatingException, e:
        current_app.logger.error(traceback.format_exc())
        return 'ERROR: ' + e.message
    except:
        current_app.logger.error(traceback.format_exc())
        return 'ERROR: unknown error'


#
# @brief: add or modify account
# @route: /ajax/account_manager
# @accepted methods: [post]
# @allowed user: administrator or the user
# @ajax return: string
#
@ajax.route('/ajax/account_manager', methods=['POST'])
@login_required
def account_manager():
    try:
        profile_user = user_server.get_by_username_or_404(request.args['username'])
    except:
        profile_user = current_user
    account_form = form.AccountForm()
    if current_user != profile_user and\
            (not current_user.is_admin and not current_user.is_coach_of(profile_user)):
        return u"没有权限"
    if account_form.validate_on_submit():
        try:
            has_account = Account.query\
                    .filter_by(user=profile_user, oj_name=account_form.oj_name.data)\
                    .first()
            if has_account:
                account_server.modify_account(has_account, account_form)
                return u"ok"
            else:
                account_server.add_account(profile_user, account_form)
                return u"ok"
        except AccountUpdatingException, e:
            current_app.logger.error(traceback.format_exc())
            return 'ERROR: ' + e.message
        except AccountExistException, e:
            current_app.logger.error(traceback.format_exc())
            return 'ERROR: ' + e.message
        except:
            current_app.logger.error(traceback.format_exc())
            return 'ERROR: unknown error'
    else:
        return u"添加账号失败"


#
# @brief: delete account
# @route: /ajax/delete_account
# @accepted methods: [post]
# @allowed user: administrator or the user
# @ajax return: string
#
@ajax.route('/ajax/delete_account', methods=['POST'])
@login_required
def delete_account():
    try:
        profile_user = user_server.get_by_id(request.form.get('user_id'))
    except:
        profile_user = current_user
    if profile_user != current_user and\
            (not current_user.is_admin and not current_user.is_coach_of(profile_user)):
        return u"没有权限"
    try:
        account_id = request.form.get('account_id')
        account_server.delete_account_by_id(profile_user, account_id)
        return u"OK"
    except AccountUpdatingException, e:
        current_app.logger.error(traceback.format_exc())
        return 'ERROR: ' + e.message
    except:
        current_app.logger.error(traceback.format_exc())
        return 'ERROR: unknown error'




#
# @brief: add or modify solution
# @route: /ajax/solution_manager
# @accepted methods: [post]
# @allowed user: administrator or the user
# @ajax return: string
#
@ajax.route('/ajax/solution_manager', methods=['POST'])
@login_required
def solution_manager():
    try:
        profile_user = user_server.get_by_username_or_404(request.args['username'])
    except:
        profile_user = current_user
    solution_form = form.SolutionForm()
    if solution_form.validate_on_submit():
        try:
            is_draft = int(request.args['draft'])
            article_server.post(solution_form, profile_user, is_draft)
            return u"发表成功!"
        except Exception, e:
            current_app.logger.error(traceback.format_exc())
            return u"发表文章失败" + e.message
    else:
        return u"发表文章失败,请检查内容"


#
# @brief: ajax to get status list
# @route: /ajax/fitch_status/<oj_name>
# @allowed user: all
#
@ajax.route('/ajax/fitch_status/<oj_name>', methods=['POST'])
@login_required
def fitch_status(oj_name):
    headers = ['account_name', 'run_id', 'pro_id', 'lang', 'run_time', 'memory', 'submit_time']
    ret = status_server.DataTablesServer(request.form, oj_name, headers).run_query()
    return json.dumps(ret, cls=CJsonEncoder)




#
# @brief: ajax html for one img choose item
# @allowed user: admin and coach
#
@login_required
def get_img_choose_item(img_item):
    return render_template('ajax/img-choose-item.html',
                           img_item = img_item,
                           file_url = resource_server.file_url)


#
# @brief: ajax img choose list
# @route: /ajax/img_choose_list
# @allowed user: admin and coach
#
@ajax.route('/ajax/img_choose_list', methods=["POST"])
@login_required
def get_img_choose_list():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    offset = request.form.get('offset')
    limit = request.form.get('limit')
    type = request.form.get('type')
    from dao.dbResource import ResourceUsage
    if type == 'honor':
        images = resource_server.get_image_list(offset, limit, ResourceUsage.HONOR_RES)
        sum = resource_server.get_image_count(ResourceUsage.HONOR_RES)
    else:
        images = resource_server.get_image_list(offset, limit)
        sum = resource_server.get_image_count()
    return jsonify(img_list=[get_img_choose_item(img) for img in images],
                   sum=sum, offset=int(offset), limit=len(images))



#
# @brief: ajax html for one resource item
# @allowed user: self, admin and coach
#
@login_required
def get_resource_list_item(resource):
    return render_template('ajax/resource_list_item.html',
                           resource = resource,
                           file_size = resource_server.file_size,
                           file_url = resource_server.file_url)


#
# @brief: ajax resource list
# @route: /ajax/resource_list
# @accepted methods: [post]
# @allowed user: self, admin, coach
#
@ajax.route('/ajax/resource_list', methods=['GET', 'POST'])
@login_required
def get_resource_list():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', None)
    per_page = RESOURCE_MANAGE_PER_PAGE
    pagination = resource_server.get_list_pageable(page, per_page, current_user, search)
    page_list = list(pagination.iter_pages(left_current=1, right_current=2))
    return jsonify(items=[get_resource_list_item(resource) for resource in pagination.items],
                   prev_num=pagination.prev_num,
                   next_num=pagination.next_num,
                   page_list=page_list,
                   page=pagination.page,
                   pages=pagination.pages)


#
# @brief: ajax to upload resource
# @route: /ajax/upload
# @accepted methods: [post]
#
@ajax.route('/ajax/upload', methods=['POST'])
@login_required
def upload():
    file_form = form.FileUploadForm()
    if file_form.validate_on_submit():
        try:
            if file_form.upload.data:
                file = request.files[file_form.upload.name]
                msg = resource_server.save_file(file_form, file, current_user, 'other')
                return msg
            else:
                return u'上传数据失败'
        except Exception, e:
            current_app.logger.error(traceback.format_exc())
            return u'错误: ' + e.message
    return u'数据填写有误'


#
# @brief: ajax to upload poster
# @route: /ajax/upload
# @accepted methods: [post]
#
@ajax.route('/ajax/upload/poster', methods=['POST'])
@login_required
def upload_poster():
    from dao.dbResource import ResourceLevel, ResourceUsage
    file_form = form.FileUploadForm()
    file_form.level.data = str(ResourceLevel.PUBLIC)
    file_form.usage.data = str(ResourceUsage.POSTER_RES)
    if file_form.validate_on_submit():
        try:
            file_canvas = request.form.get('croppedImage')
            if file_canvas:
                file_string = re.sub('^data:image/.+;base64,', '', file_canvas).decode('base64')
                file_binary = cStringIO.StringIO(file_string)
                file = FileStorage(file_binary, file_form.name.data + '.jpg')
                msg = resource_server.save_file(file_form, file, current_user, 'poster')
                return msg
            else:
                return u'上传数据失败'
        except Exception, e:
            current_app.logger.error(traceback.format_exc())
            return u'错误: ' + e.message
    current_app.logger.error(file_form.errors)
    return u'数据填写有误'


#
# @brief: ajax to get modal with edit-resource form
# @route: /ajax/resource_info
# @accepted methods: [post]
#
@ajax.route('/ajax/resource_info', methods=['POST'])
@login_required
def get_resource_info():
    resource_id = request.form.get('resource_id')
    rs = resource_server.get_by_id(resource_id)
    if rs.level >= 2 and not current_user.is_admin and not current_user.is_coach_of(rs.user):
        return u'permission denied'
    file_edit_form = form.FileInfoForm()
    if not current_user.is_admin and not current_user.is_coach:
        file_edit_form.usage.choices = [('3',u'题解资源'), ('4',u'其他资源')]
    file_edit_form.id.data = rs.id
    file_edit_form.level.data = str(rs.level)
    file_edit_form.name.data = rs.name
    file_edit_form.description.data = rs.description
    file_edit_form.usage.data = str(rs.usage)
    return render_template('ajax/resource_modify_modal.html',
                           file_edit_form = file_edit_form)


#
# @brief: ajax to edit resource
# @route: /ajax/resource_info
# @accepted methods: [post]
#
@ajax.route("/ajax/edit_resource", methods = ['POST'])
@login_required
def edit_resource():
    file_edit_form = form.FileInfoForm()
    if file_edit_form.validate_on_submit():
        return resource_server.modify_file(file_edit_form, current_user)
    return u'表单填写错误'


#
# @brief: ajax to delete resource
# @route: /ajax/delete_resource
# @accepted methods: [post]
#
@ajax.route("/ajax/delete_resource", methods = ['POST'])
@login_required
def delete_resource():
    try:
        resource_id = request.form.get('resource_id')
        msg = resource_server.delete_file(resource_id, current_user)
        return msg
    except:
        current_app.logger.error(traceback.format_exc())
        return u'删除失败'


#
# @brief: ajax html for one honor item
# @allowed user: self, admin and coach
#
@login_required
def get_honor_list_item(honor):
    from config import HONOR_LEVEL_MAP
    return render_template('ajax/honor_list_item.html',
                           honor = honor,
                           level_mapper = HONOR_LEVEL_MAP)


#
# @brief: ajax honor list
# @route: /ajax/honor_list
# @accepted methods: [post]
# @allowed user: self, admin, coach
#
@ajax.route('/ajax/honor_list', methods=['GET', 'POST'])
@login_required
def get_honor_list():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', None)
    per_page = HONOR_MANAGE_PER_PAGE
    pagination = honor_server.get_list_pageable(page, per_page, search)
    page_list = list(pagination.iter_pages(left_current=1, right_current=2))
    return jsonify(items=[get_honor_list_item(honor) for honor in pagination.items],
                   prev_num=pagination.prev_num,
                   next_num=pagination.next_num,
                   page_list=page_list,
                   page=pagination.page,
                   pages=pagination.pages)


#
# @brief: ajax to add honor
# @route: /ajax/add_honor
# @accepted methods: [post]
# @allowed user: self, admin, coach
#
@ajax.route("/ajax/add_honor", methods = ['POST'])
@login_required
def add_honor():
    honor_form = form.HonorForm()
    file_form = form.FileUploadForm()
    honor_form.users.choices = user_server.get_user_choice()
    if honor_form.validate_on_submit():
        try:
            from dao.dbResource import ResourceLevel, ResourceUsage
            resource_list = []
            for name, file in request.files.items(multi=True):
                file_form.level.data = ResourceLevel.PUBLIC
                file_form.name.data = unicode(file.filename).split('.')[0]
                file_form.usage.data = ResourceUsage.HONOR_RES
                resource_server.save_file(file_form, file, current_user, 'honor')
                resource = resource_server.get_by_name(file_form.name.data)
                resource_list.append(resource)
            msg = honor_server.add_honor(honor_form, resource_list)
            return msg
        except Exception, e:
            current_app.logger.error(traceback.format_exc())
            return 'failed'
    return u'数据填写有误'



#
# @brief: ajax to modify honor
# @route: /ajax/modify_honor
# @accepted methods: [post]
# @allowed user: self, admin, coach
#
@ajax.route("/ajax/modify_honor", methods = ['POST'])
@login_required
def modify_honor():
    honor_form = form.HonorForm()
    file_form = form.FileUploadForm()
    honor_form.users.choices = user_server.get_user_choice()
    if honor_form.validate_on_submit():
        try:
            honor = honor_server.get_by_id(honor_form.id.data)
            from dao.dbResource import ResourceLevel, ResourceUsage
            resource_list = []
            for name, file in request.files.items(multi=True):
                if file.filename == '':
                    continue
                file_form.level.data = ResourceLevel.PUBLIC
                file_form.name.data = unicode(file.filename).split('.')[0]
                file_form.usage.data = ResourceUsage.HONOR_RES
                ret = resource_server.save_file(file_form, file, current_user, 'honor')
                if ret == 'OK':
                    resource = resource_server.get_by_name(file_form.name.data)
                    resource_list.append(resource)
            msg = honor_server.modify_honor(honor, honor_form, resource_list)
            return msg
        except:
            current_app.logger.error(traceback.format_exc())
            return 'failed'
    return u'数据填写有误'



#
# @brief: ajax to delete honor
# @route: /ajax/delete_honor
# @accepted methods: [post]
# @allowed user: self, admin, coach
#
@ajax.route("/ajax/delete_honor", methods = ['POST'])
@login_required
def delete_honor():
    try:
        honor_id = request.form.get('honor_id')
        msg = honor_server.delete_honor(honor_id)
        return msg
    except:
        current_app.logger.error(traceback.format_exc())
        return u'FAIL'


# not used
@login_required
def get_article_list_item(article):
    return render_template('ajax/article_list_item.html', article = article)


#
# @brief: ajax article list
# @route: /ajax/article_list
# @accepted methods: [post]
# @allowed user: self, admin, coach
#
@ajax.route("/ajax/article_list", methods = ['POST'])
@login_required
def get_article_list():
    offset = request.form.get('offset')
    limit = request.form.get('limit')
    article_list = article_server.get_list(offset, limit, current_user)
    sum = article_server.get_count(current_user)
    return jsonify(article_list=[get_article_list_item(article) for article in article_list],
                   sum=sum, offset=int(offset), limit=len(article_list))


# not used
@login_required
def get_related_submits_item(submit):
    return render_template('ajax/related_submits_item.html', submit=submit)


# not used
@ajax.route("/ajax/related_submits", methods = ['POST'])
@login_required
def get_related_submits():
    article_id = request.form.get('article_id')
    offset = request.form.get('offset')
    limit = request.form.get('limit')
    one = article_server.get_by_id(article_id)
    related_submits = article_server.related_submits(one, offset, limit)
    sum = article_server.related_submits_count(one)
    return jsonify(submits_list=[get_related_submits_item(submit) for submit in related_submits],
                   sum=sum, offset=int(offset), limit=len(related_submits))


# not used
@login_required
def get_related_article_item(article):
    return render_template('ajax/related_article_item.html', article=article)


# not used
@ajax.route("/ajax/related_article", methods = ['POST'])
@login_required
def get_related_article():
    submit_id = request.form.get('submit_id')
    offset = request.form.get('offset')
    limit = request.form.get('limit')
    one = general.get_submit_by_id(submit_id)
    related_article = general.related_article(one, offset, limit)
    sum = general.related_article_count(one)
    return jsonify(article_list=[get_related_article_item(article) for article in related_article],
                   sum=sum, offset=int(offset), limit=len(related_article))


#
# @brief: ajax to delete article
# @route: /ajax/delete_article
# @accepted methods: [post]
# @allowed user: self, admin, coach
#
@ajax.route("/ajax/delete_article", methods = ['POST'])
@login_required
def delete_article():
    try:
        article_id = request.form.get('article_id')
        article_server.delete_by_id(article_id)
        return u'删除成功'
    except Exception, e:
        current_app.logger.error(traceback.format_exc())
        return u'删除失败'


#
# @brief: ajax to get member situation list
# @route: /ajax/members
# @accepted methods: [get]
# @allowed user: public
#
@ajax.route("/ajax/members", methods=['GET'])
def members():
    all_users = user_server.get_list(limit=-1)
    users = []
    for user in all_users:
        if user.is_student:
            users.append({
                'name': user.name,
                'college': SCHOOL_COLLEGE_MAP[user.college] if user.college else '',
                'grade': user.grade + u'级' if user.grade else '',
                'situation': user.situation
            })
    return json.dumps({ 'data': users })


#
# @brief: ajax html for one competition item
# @allowed user: admin and coach
#
@login_required
def get_competition_list_item(competition):
    from datetime import datetime
    diff = (competition.event_date - datetime.today()).days
    if diff > 2:
        process = 0
    elif diff > -1:
        process = 1
    else:
        process = 2
    return render_template('ajax/competition_list_item.html',
                           competition = competition,
                           len = len, process = process)


#
# @brief: ajax competition list
# @route: /ajax/competition_list
# @allowed user: admin and coach
#
@ajax.route('/ajax/competition_list', methods=["GET", "POST"])
@login_required
def get_competitions():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', None)
    per_page = COMPETITION_MANAGE_PER_PAGE
    pagination = dbCompetition.get_list_pageable(page, per_page, search=search)
    page_list = list(pagination.iter_pages(left_current=1, right_current=2))
    return jsonify(items=[get_competition_list_item(c) for c in pagination.items],
                   prev_num=pagination.prev_num,
                   next_num=pagination.next_num,
                   page_list=page_list,
                   page=pagination.page,
                   pages=pagination.pages)


@ajax.route("/ajax/add_competition", methods = ['POST'])
@login_required
def add_competition():
    competition_form = form.CompetitionForm()
    if competition_form.validate_on_submit():
        try:
            feedback = dbCompetition.create_competition(competition_form)
            if feedback == 'OK':
                return '添加成功'
            else:
                return feedback
        except Exception, e:
            current_app.logger.error(traceback.format_exc())
            return u'添加失败'
    return u'数据填写有误'


@ajax.route("/ajax/edit_competition", methods = ['POST'])
@login_required
def edit_competition():
    competition_form = form.CompetitionForm()
    if competition_form.validate_on_submit():
        try:
            id = request.form.get('id')
            feedback = dbCompetition.update_competition(id, competition_form)
            if feedback == 'OK':
                return '修改成功'
        except Exception, e:
            current_app.logger.error(traceback.format_exc())
            return u'修改失败'
    return u'数据填写有误'


@ajax.route("/ajax/delete_competition", methods = ['POST'])
@login_required
def delete_competition():
    try:
        competition_id = request.form.get('competition_id', -1, type=int)
        dbCompetition.delete_by_id(competition_id)
        return u'OK'
    except Exception, e:
        current_app.logger.error(traceback.format_exc())
        return u'删除失败'


#
# @brief: ajax html for one player item
# @allowed user: admin and coach
#
@login_required
def get_player_list_item(player):
    return render_template('ajax/player_list_item.html',
                           player = player,
                           college_mapper = SCHOOL_COLLEGE_MAP)


#
# @brief: ajax player list
# @route: /ajax/player_list
# @allowed user: admin and coach
#
@ajax.route('/ajax/player_list', methods=["GET", "POST"])
@login_required
def get_players():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', None)
    competition_id = request.args.get('competition', 1, type=int)
    per_page = COMPETITION_MANAGE_PER_PAGE

    competition = dbCompetition.get_by_id(competition_id)
    pagination = dbCompetition.get_players_pageable(competition, page,
                                                    per_page, search=search)
    page_list = list(pagination.iter_pages(left_current=1, right_current=2))
    return jsonify(items=[get_player_list_item(p) for p in pagination.items],
                   prev_num=pagination.prev_num,
                   next_num=pagination.next_num,
                   page_list=page_list,
                   page=pagination.page,
                   pages=pagination.pages)


@ajax.route("/ajax/delete_player", methods = ['POST'])
@login_required
def delete_player():
    try:
        player_id = request.form.get('player_id', -1, type=int)
        dbPlayer.delete_by_id(player_id)
        return u'OK'
    except Exception, e:
        current_app.logger.error(traceback.format_exc())
        return u'删除失败'