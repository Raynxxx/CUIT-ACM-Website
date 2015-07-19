# coding=utf-8
import os
from __init__ import *
from server import user_server, solution_server, status_server, form, account_server, book_server, news_server
from dao.dbACCOUNT import Account
from util import json, CJsonEncoder
from werkzeug.utils import secure_filename
#
# @blueprint: ajax
# @created: 2015/06/22
# @author: Z2Y
#
ajax = blueprints.Blueprint('ajax', __name__)

#
# @brief: add user
# @route: /register
# @accepted methods: [post]
# @allowed user: administrator
# @ajax return: 用户是否添加成功 => string
#
@ajax.route('/register', methods=["POST"])
@login_required
def register():
    if not current_user.rights:
        flash(u"你没有权限访问该模块")
        return redirect(url_for('index'))
    reg_form = form.RegisterForm()
    if reg_form.validate_on_submit():
        try:
            user_server.UserServer.addUser(reg_form)
            return u"添加用户成功"
        except Exception, e:
            return u"添加用户失败:" + e.message
    else:
        return u"添加用户失败:表单填写有误。"


@ajax.route('/modify_userinfo', methods=['POST'])
@login_required
def modify_userinfo():
    user = user_server.UserServer(current_user)
    user_modify_form = form.UserModifyForm()
    if user_modify_form.validate_on_submit():
        try:
            user.modify_info(user_modify_form)
            return u"修改资料成功"
        except Exception, e:
            return u'修改资料失败' + e.message
    else:
        return u"修改资料失败:表单填写有误"



#
# @brief: modify password
# @route: /modify_pwd
# @accepted methods: [post]
# @allowed user: administrator or the user
# @ajax return: 密码是否修改成功 => string
#
@ajax.route('/modify_pwd', methods=['POST'])
@login_required
def modify_pwd():
    user = user_server.UserServer(current_user)
    pwd_form = form.PasswordModifyForm()
    if pwd_form.validate_on_submit():
        return user.modify_password(pwd_form)
    return u"修改密码失败"

#
# @brief: add or modify account
# @route: /account_manager
# @accepted methods: [post]
# @allowed user: administrator or the user
# @ajax return: string
#
@ajax.route('/ajax/account_manager', methods=['POST'])
@login_required
def account_manager():
    try:
        profile_user = user_server.UserServer.loadUser_or_404(request.args['username'])
    except:
        profile_user = current_user
    account_form = form.AccountForm()
    if account_form.validate_on_submit():
        has = Account.query.filter_by(user=profile_user, oj_name=account_form.oj_name.data).first()
        if has:
            account_server.modify_account(has, account_form)
            return u"已经覆盖原账号"
        else:
            account_server.add_account(profile_user, account_form)
            return u"添加账号成功"
    else:
        return u"添加账号失败"


@ajax.route('/ajax/delete_account', methods=['POST'])
@login_required
def delete_account():
    try:
        profile_user = user_server.UserServer.loadUser_or_404(request.args['username'])
    except:
        profile_user = current_user
    try:
        oj_name = request.args['oj_name']
        account_server.delete_account(profile_user, oj_name)
        return 'OK'
    except:
        return 'ERROR'


#
# @brief: add or modify solution
# @route: /solution_manager
# @accepted methods: [post]
# @allowed user: administrator or the user
# @ajax return: string
#
@ajax.route('/ajax/solution_manager', methods=['POST'])
@login_required
def solution_manager():
    try:
        profile_user = user_server.UserServer.loadUser_or_404(request.args['username'])
    except:
        profile_user = current_user
    solution_form = form.SolutionForm()
    if solution_form.validate_on_submit():
        try:
            solution_server.post(solution_form, profile_user)
            return u"发表成功!"
        except Exception, e:
            return u"发表文章失败" + e.message
    else:
        return u"发表文章失败,请检查内容"

@ajax.route('/ajax/news_manager', methods=['POST'])
@login_required
def news_manager():
    if not current_user.rights:
        return u"没有权限"
    news_form = form.NewsForm()
    if news_form.validate_on_submit():
        try:
            news_server.post(news_form, current_user)
            return u"发表成功!"
        except Exception, e:
            return u"发表新闻失败" + e.message
    else:
        return u"发表新闻失败,请检查内容"


@ajax.route('/ajax/account_info', methods=['POST', 'GET'])
@login_required
def account_info():
    try:
        profile_user = user_server.UserServer.loadUser_or_404(request.args['username'])
    except:
        profile_user = current_user
    data = account_server.get_account_info(profile_user)
    return json.dumps(data, cls=CJsonEncoder)

@ajax.route('/ajax//fitch_status/<oj_name>', methods=['POST'])
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
                book_form.shortcut.data = os.path.join(IMAGE_FILE_PATH,filename)
                file.save(book_form.shortcut.data)
            book_server.add_book(book_form)
            return 'ok'
        except Exception, e:
            return 'error:' + e.message
    return 'error:数据填写有误'


