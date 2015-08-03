# coding=utf-8
import os
from __init__ import *
from server import user_server, article_server, status_server, form, account_server, book_server, news_server, resource_server
from dao.dbACCOUNT import Account
from util import json, CJsonEncoder
from werkzeug.utils import secure_filename
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from server.account_server import AccountUpdatingException, AccountExistException

#
# @blueprint: ajax
# @created: 2015/06/22
# @author: Z2Y
#
ajax = blueprints.Blueprint('ajax', __name__)


#
# @brief: ajax html for one user item
# @allowed user: admin and coach
#
@login_required
def get_user_list_item(user):
    return render_template('ajax/user_list_item.html',
                           user = user,
                           school_mapper = SCHOOL_MAP)

#
# @brief: ajax user list
# @route: /ajax/user_list
# @allowed user: admin and coach
#
@ajax.route('/ajax/user_list', methods=["POST"])
@login_required
def get_user_list():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('index'))
    offset = request.form.get('offset')
    limit = request.form.get('limit')
    users = list()
    sum = 0
    if current_user.is_admin:
        users = user_server.get_list(offset, limit)
        sum = user_server.get_count()
    elif current_user.is_coach:
        users = user_server.get_list(offset, limit, school=current_user.school)
        sum = user_server.get_count(school=current_user.school)
    return jsonify(user_list=[get_user_list_item(user) for user in users],
                   sum=sum, offset=int(offset), limit=len(users))

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
            return u"添加用户失败: " + e.message
    else:
        #print reg_form.errors
        return u"添加用户失败: 表单填写有误"

@ajax.route('/ajax/create_users', methods=["POST"])
@login_required
def create_users():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    reg_form = form.MultiRegisterForm()
    if reg_form.validate_on_submit():
        try:
            ret = user_server.create_mul_users(reg_form, current_user)
            return ret
        except Exception, e:
            return u"添加用户失败: " + e.message
    else:
        #print reg_form.errors
        return u"添加用户失败: 表单填写有误"


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
        print u"你没有权限访问该模块"
        return redirect(url_for('main.index'))
    try:
        id = request.form.get('user_id')
        user_server.delete_by_id(id)
        return "删除用户成功"
    except Exception, e:
        return u"删除用户失败: " + e.message

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
@ajax.route('/ajax/news_list', methods=['POST'])
@login_required
def get_news_list():
    if not current_user.is_admin and not current_user.is_coach:
        print "你没有权限访问该模块"
        return redirect(url_for('main.index'))

    news_list = list()
    sum = 0
    offset = request.form.get('offset')
    limit = request.form.get('limit')
    if current_user.is_admin:
        news_list = news_server.get_list(offset, limit, show_draft=True)
        sum = news_server.get_count(show_draft=True)
    elif current_user.is_coach:
        news_list = news_server.get_list(offset, limit, show_draft=True, coach=current_user)
        sum = news_server.get_count(show_draft=True, coach=current_user)
    return jsonify(news_list=[get_news_list_item(news) for news in news_list],
                   sum=sum, offset=int(offset), limit=len(news_list))


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
        return u'删除成功'
    except:
        return u'删除失败'

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
            return u"发表新闻失败: 固定链接已存在"
        except Exception, e:
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
        return 'ERROR: ' + e.message
    except:
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
            return 'ERROR: ' + e.message
        except AccountExistException, e:
            return 'ERROR: ' + e.message
        except:
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
        return u"ok"
    except AccountUpdatingException, e:
        return 'ERROR: ' + e.message
    except:
        return 'ERROR: unknown error'



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
        return redirect(url_for('index'))
    offset = request.form.get('offset')
    limit = request.form.get('limit')
    from dao.dbResource import ResourceType
    images = resource_server.get_list(offset, limit, current_user, type=ResourceType.IMAGES)
    sum = resource_server.get_count(current_user, type=ResourceType.IMAGES)
    return jsonify(img_list=[get_img_choose_item(img) for img in images],
                   sum=sum, offset=int(offset), limit=len(images))



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
            article_server.post(solution_form, profile_user)
            return u"发表成功!"
        except Exception, e:
            return u"发表文章失败" + e.message
    else:
        return u"发表文章失败,请检查内容"



@ajax.route('/ajax/fitch_status/<oj_name>', methods=['POST'])
@login_required
def fitch_status(oj_name):
    headers = ['account_name', 'run_id', 'pro_id', 'lang', 'run_time', 'memory', 'submit_time']
    ret = status_server.DataTablesServer(request.form, oj_name, headers).run_query()
    return json.dumps(ret, cls=CJsonEncoder)


@ajax.route('/ajax/add_book', methods=['POST'])
@login_required
def add_book():
    book_form = form.BookForm()
    if book_form.validate_on_submit():
        try:
            book_form.shortcut.data = ''
            if book_form.upload.data:
                file = request.files[book_form.upload.name]
                filename = secure_filename(file.filename)
                book_form.shortcut.data = os.path.join(IMAGE_FILE_PATH, filename)
                file.save(book_form.shortcut.data)
            book_server.add_book(book_form)
            return 'ok'
        except Exception, e:
            return 'error:' + e.message
    return 'error:数据填写有误'


#
# @brief: ajax html for one resource item
# @allowed user: self, admin and coach
#
@login_required
def get_resource_list_item(resource):
    return render_template('ajax/resource_list_item.html',
                           resource = resource,
                           file_size = resource_server.file_size)


@ajax.route('/ajax/resource_info', methods=['POST'])
@login_required
def get_resource_info():
    resource_id = request.form.get('resource_id')
    rs = resource_server.get_by_id(resource_id)
    if rs.level >= 2 and not current_user.is_admin and not current_user.is_coach_of(rs.user):
        return u'permission denied'
    file_edit_form = form.FileInfoForm()
    file_edit_form.id.data = rs.id
    file_edit_form.level.data = str(rs.level)
    file_edit_form.name.data = rs.name
    file_edit_form.description.data = rs.description
    file_edit_form.usage.data = str(rs.usage)
    return render_template('ajax/resource_modify_modal.html',file_edit_form = file_edit_form)


#
# @brief: ajax resource list
# @route: /ajax/resource_list
# @accepted methods: [post]
# @allowed user: self, admin, coach
#
@ajax.route('/ajax/resource_list', methods=['POST'])
@login_required
def get_resource_list():
    offset = request.form.get('offset')
    limit = request.form.get('limit')
    resource_list = resource_server.get_list(offset, limit, current_user)
    sum = resource_server.get_count(current_user)
    return jsonify(news_list=[get_resource_list_item(resource) for resource in resource_list],
                   sum=sum, offset=int(offset), limit=len(resource_list))

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
                msg = resource_server.save_file(file_form, file, current_user)
                return msg
            else:
                return u'上传数据失败'
        except Exception, e:
            return u'错误: ' + e.message
    return u'数据填写有误'


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
        return u'删除失败'

@ajax.route("/ajax/edit_resource", methods = ['POST'])
@login_required
def edit_resource():
    file_edit_form = form.FileInfoForm()
    if file_edit_form.validate_on_submit():
        return resource_server.modify_file(file_edit_form, current_user)
    return u'表单填写错误'







