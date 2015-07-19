# coding=utf-8
from __init__ import *
from server import general, user_server, form, news_server

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
    if not current_user.rights:
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
    if not current_user.rights:
        return redirect(url_for('main.index'))
    sys = general.get_sys_info()
    return render_template('sys_info.html', sys=sys)

#
# @brief: the page for administrator to manage user
# @route: /admin/manage_user
# @accepted methods: [get]
# @allowed user: administrator
#
@admin.route('/admin/manage_user', methods=["get"])
@login_required
def manage_user():
    if not current_user.rights:
        return redirect(url_for('main.index'))
    user_add_form = form.RegisterForm()
    pwd_modify_form = form.PasswordModifyForm()
    return render_template('add_user.html', form1=user_add_form, form2=pwd_modify_form)

@admin.route("/admin/add_book", methods = ['GET'])
@login_required
def add_book():
    if not current_user.rights:
        return redirect(url_for('main.index'))
    bookform = form.BookForm()
    return render_template('add_book.html', bookform=bookform)

@admin.route("/admin/post_news", methods = ['GET'])
@login_required
def post_news():
    if not current_user.rights:
        return redirect(url_for('main.index'))
    newsform = form.NewsForm()
    return render_template('post_news.html', form=newsform)

@admin.route("/admin/edit_news", methods = ['GET'])
@login_required
def edit_news():
    if not current_user.rights:
        return redirect(url_for('main.index'))
    try:
        one = news_server.get_one(request.args['p'])
        if one.user != current_user:
            raise Exception(u"你没有权限修改该文章")
    except :
        return redirect(url_for('main.index'))
    news_form = form.NewsForm()
    if one:
        news_form.sid.data = one.id
        news_form.title.data = one.title
        news_form.shortcut.data = one.shortcut
        news_form.content.data = one.content
        news_form.url.data = one.url
        news_form.istop.data = one.istop
        tags = []
        for tag in one.tags:
            tags.append(tag.__repr__())
        news_form.tags.data = tags
    return render_template('post_news.html', form=news_form)

