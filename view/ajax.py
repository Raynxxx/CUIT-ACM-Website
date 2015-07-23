# coding=utf-8
import os
from __init__ import *
from server import user_server, article_server, status_server, form, account_server, book_server, news_server
from dao.dbACCOUNT import Account
from util import json, CJsonEncoder
from werkzeug.utils import secure_filename
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from server.account_server import AccountUpdatingException

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
    return render_template('ajax/user_list_item.html', user=user)

#
# @brief: ajax user list
# @allowed user: admin and coach
#
@ajax.route('/user_list', methods=["POST"])
@login_required
def get_user_list():
    if not current_user.is_admin and not current_user.is_coach:
        print u"你没有权限访问该模块"
        return redirect(url_for('index'))
    global users, sum
    offset = request.form.get('offset')
    limit = request.form.get('limit')
    if current_user.is_admin:
        users = user_server.get_list(offset, limit)
        sum = user_server.get_count()
    if not current_user.is_admin and current_user.is_coach:
        users = user_server.get_list(offset, limit, is_admin=False, school=current_user.school)
        sum = user_server.get_count(is_admin=False, school=current_user.school)
    return jsonify(user_list=[get_user_list_item(user) for user in users],
                   sum=sum, offset=int(offset), limit=len(users))

#
# @brief: add user
# @route: /register
# @accepted methods: [post]
# @allowed user: admin and coach
# @ajax return: 用户是否添加成功
#
@ajax.route('/register', methods=["POST"])
@login_required
def register():
    if not current_user.is_admin and not current_user.is_coach:
        print u"你没有权限访问该模块"
        return redirect(url_for('index'))
    reg_form = form.RegisterForm()
    rights_list = request.form.getlist('rights')
    #print rights_list
    rights = 0
    for item in rights_list:
        rights = rights | int(item)
    #print rights
    if reg_form.validate_on_submit():
        try:
            ret = user_server.create_user(reg_form, rights)
            if ret == 'ok':
                return u"添加用户成功"
            return ret
        except Exception, e:
            return u"添加用户失败: " + e.message
    else:
        #print reg_form.errors
        return u"添加用户失败: 表单填写有误"


#
# @brief: delete user
# @route: /delete_user
# @accepted methods: [post]
# @allowed user: admin and coach
#
@ajax.route('/delete_user', methods=["POST"])
@login_required
def delete_user():
    if not current_user.is_admin and not current_user.is_coach:
        print u"你没有权限访问该模块"
        return redirect(url_for('index'))
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
# @allowed user: administrator
#
@ajax.route('/ajax/news_list', methods=['POST'])
@login_required
def get_news_list():
    if not current_user.is_admin and not current_user.is_coach:
        print "你没有权限访问该模块"
        return redirect(url_for('main.index'))

    offset = request.form.get('offset')
    limit = request.form.get('limit')
    news_list = news_server.get_list(offset, limit, show_draft=True)
    sum = news_server.get_count(show_draft=True)
    return jsonify(news_list=[get_news_list_item(news) for news in news_list],
                   sum=sum, offset=int(offset), limit=len(news_list))


#
# @brief: delete news
# @route: /delete_news
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
# @route: /post_news
# @accepted methods: [post]
# @allowed user: admin and coach
#
@ajax.route('/ajax/post_news', methods=['POST'])
@login_required
def post_news():
    if not current_user.rights:
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
            return u"发表新闻失败" + e.message
    else:
        return u"发表新闻失败,请检查内容"


#
# @brief: modify user's info
# @route: /modify_userinfo
# @accepted methods: [post]
# @allowed user: administrator
# @ajax return:
#
@ajax.route('/modify_userinfo', methods=['POST'])
@login_required
def modify_userinfo():
    user_modify_form = form.UserModifyForm()
    if user_modify_form.validate_on_submit():
        try:
            user_server.modify_info(current_user, user_modify_form)
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
    pwd_form = form.PasswordModifyForm()
    if pwd_form.validate_on_submit():
        return user_server.modify_password(current_user, pwd_form)
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
        profile_user = user_server.get_by_username_or_404(request.args['username'])
    except:
        profile_user = current_user
    account_form = form.AccountForm()
    if account_form.validate_on_submit():
        try:
            has = Account.query.filter_by(user=profile_user, oj_name=account_form.oj_name.data).first()
            if has:
                account_server.modify_account(has, account_form)
                return u"已经覆盖原账号"
            else:
                account_server.add_account(profile_user, account_form)
                return u"添加账号成功"
        except AccountUpdatingException, e:
            return 'ERROR: ' + e.message
        except:
            return 'ERROR: unknown error'
    else:
        return u"添加账号失败"


@ajax.route('/ajax/delete_account', methods=['POST'])
@login_required
def delete_account():
    try:
        profile_user = user_server.get_by_username_or_404(request.args['username'])
    except:
        profile_user = current_user
    try:
        oj_name = request.args['oj_name']
        account_server.delete_account(profile_user, oj_name)
        return 'OK'
    except AccountUpdatingException, e:
        return 'ERROR: ' + e.message
    except:
        return 'ERROR: unknown error'


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


@ajax.route('/ajax/account_info', methods=['POST', 'GET'])
@login_required
def account_info():
    try:
        profile_user = user_server.get_by_username_or_404(request.args['username'])
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
                book_form.shortcut.data = os.path.join(IMAGE_FILE_PATH, filename)
                file.save(book_form.shortcut.data)
            book_server.add_book(book_form)
            return 'ok'
        except Exception, e:
            return 'error:' + e.message
    return 'error:数据填写有误'


