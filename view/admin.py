# coding=utf-8
from __init__ import *
from server import general, user_server, form, news_server
import util, config

#
# @blueprint: admin
# @created: 2015/06/22
# @author: Z2Y
#
admin = blueprints.Blueprint('admin', __name__, template_folder='../templates/admin')

#
# @brief: the index page for administrator
# @route: /admin
# @accepted methods: [get]
# @allowed user: administrator
#
@admin.route('/admin', methods=["get"])
@login_required
def index():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    return redirect(url_for('admin.sys_info'))

#
# @brief: the page for administrator to view system info
# @route: /admin/sys_info
# @accepted methods: [get]
# @allowed user: administrator
#
@admin.route('/admin/sys_info', methods=["get"])
@login_required
def sys_info():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    sys = general.get_sys_info()
    return render_template('sys_info.html', sys=sys)

#
# @brief: the page for administrator to manage users
# @route: /admin/manage_user
# @accepted methods: [get]
# @allowed user: administrator
#
@admin.route('/admin/manage_user', methods=["get"])
@login_required
def manage_user():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    return render_template('manage_user.html',
                           title = u'用户管理',
                           limit = config.USER_MANAGE_PER_PAGE)

#
# @brief: the page for administrator to manage user
# @route: /admin/manage_user
# @accepted methods: [get]
# @allowed user: admin and coach
#
@admin.route('/admin/create_user', methods=["get"])
@login_required
def create_user():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    registerForm = form.RegisterForm()
    registerForm.school.data = current_user.school
    multi_registerForm = form.MultiRegisterForm()
    return render_template('add_user.html',
                           title = u'添加用户',
                           register_form = registerForm,
                           multi_reg_form = multi_registerForm)


#
# @brief: the page for admin to edit user
# @route: /admin/edit_user
# @accepted methods: [get]
# @allowed user: admin and coach
#
@admin.route("/admin/edit_user", methods = ['GET'])
@login_required
def edit_user():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    try:
        has_one = user_server.get_by_id(request.args['p'])
    except :
        return redirect(url_for('admin.manage_user'))
    user_modify_form = form.UserModifyForm()
    if has_one:
        user_modify_form.id.data = has_one.id
        user_modify_form.name.data = has_one.name
        user_modify_form.stu_id.data = has_one.stu_id
        user_modify_form.email.data = has_one.email
        user_modify_form.phone.data = has_one.phone
        user_modify_form.motto.data = has_one.remark
        user_modify_form.situation.data = has_one.situation
        user_modify_form.school.data = has_one.school
        user_modify_form.gender.data = '1' if has_one.gender else '0'
        user_modify_form.active.data = '1' if has_one.active else '0'
    return render_template('edit_user.html',
                           title = u'修改用户信息',
                           user = has_one,
                           user_modify_form = user_modify_form)


#
# @brief: the page for admin to manage news
# @route: /admin/manage_news
# @accepted methods: [get]
# @allowed user: admin and coach
#
@admin.route("/admin/manage_news", methods = ['GET'])
@login_required
def manage_news():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('admin.index'))
    return render_template('admin/manage_news.html',
                           title=u'新闻管理',
                           limit = config.NEWS_MANAGE_PER_PAGE)


#
# @brief: the page for admin to post news
# @route: /admin/post_news
# @accepted methods: [get]
# @allowed user: admin and coach
#
@admin.route("/admin/post_news", methods = ['GET'])
@login_required
def post_news():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    news_form = form.NewsForm()
    upload_form = form.FileUploadForm()
    from dao.dbResource import ResourceLevel, ResourceUsage
    upload_form.level.data = str(ResourceLevel.PUBLIC)
    upload_form.usage.data = str(ResourceUsage.NEWS_RES)
    my_button = [u"保存草稿", u"直接发布"]
    return render_template('post_news.html',
                           title = u'发布新闻',
                           action = u'发布新闻',
                           news_form = news_form,
                           upload_form = upload_form,
                           my_button = my_button)

#
# @brief: the page for admin to edit news
# @route: /admin/edit_news
# @accepted methods: [get]
# @allowed user: admin and coach
#
@admin.route("/admin/edit_news", methods = ['GET'])
@login_required
def edit_news():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    try:
        one = news_server.get_by_id(request.args['p'])
    except:
        return redirect(url_for('admin.manage_news'))
    news_form = form.NewsForm()
    upload_form = form.FileUploadForm()
    from dao.dbResource import ResourceLevel, ResourceUsage
    upload_form.level.data = str(ResourceLevel.PUBLIC)
    upload_form.usage.data = str(ResourceUsage.NEWS_RES)
    if one:
        news_form.sid.data = one.id
        news_form.title.data = one.title
        news_form.content.data = one.shortcut + '<-more->' + one.content
        news_form.url.data = one.url
        news_form.is_top.data = one.is_top
        tags = []
        for tag in one.tags:
            tags.append(tag.__repr__())
        news_form.tags.data = tags
    if one.is_draft:
        my_button = [u"保存草稿", u"直接发布"]
    else :
        my_button = [u"保存草稿", u"提交更新"]
    return render_template('post_news.html',
                           title = u'修改新闻',
                           action = u'修改新闻',
                           news_form = news_form,
                           upload_form = upload_form,
                           my_button = my_button)



@admin.route("/admin/add_book", methods = ['GET'])
@login_required
def add_book():
    if not current_user.is_admin and not current_user.is_coach:
        return redirect(url_for('main.index'))
    book_form = form.BookForm()
    return render_template('add_book.html', book_form=book_form)

