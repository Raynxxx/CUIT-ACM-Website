# coding=utf-8
from __init__ import *
from server import user_server, general, article_server, form
from config import OJ_MAP
#
# @blueprint: profile
# @created: 2015/06/22
# @author: Z2Y
#
profile = blueprints.Blueprint('profile', __name__, template_folder='../templates/profile')


@profile.route('/profile')
@login_required
def index():
    try:
        profile_user = user_server.UserServer.loadUser_or_404(request.args['username'])
    except:
        profile_user = current_user
    user = user_server.UserServer(profile_user)
    stat = user.get_statistic()
    return render_template('user_info.html', title=u'你的主页',
                           user=profile_user,
                           stat=stat)

@profile.route('/profile/stat_graph', methods=['GET'])
@login_required
def stat_graph():
    try:
        profile_user = user_server.UserServer.loadUser_or_404(request.args['username'])
    except:
        profile_user = current_user
    user = user_server.UserServer(profile_user)
    account_info = user.get_account_info()
    general_info = {}
    for oj in account_info['have']:
        tmp = user.get_general_info(oj)
        if tmp:
            general_info[oj] = tmp
    return render_template('stat_graph.html', account_info=account_info, user=profile_user
                           , OJ_MAP=OJ_MAP, str=str, general_info=general_info)

@profile.route('/profile/manage_account', methods=['GET'])
@login_required
def manage_account():
    try:
        profile_user = user_server.UserServer.loadUser_or_404(request.args['username'])
    except:
        profile_user = current_user
    account_form = form.AccountForm()
    return render_template('manage_account.html', form=account_form, user=profile_user)


@profile.route('/profile/update_account', methods=['GET'])
@login_required
def update_account():
    try:
        profile_user = user_server.UserServer.loadUser_or_404(request.args['username'])
    except:
        profile_user = current_user
    general.update_user_status(profile_user)
    return redirect(url_for('profile.index', username=profile_user.username))


@profile.route('/profile/modify_info', methods=['GET'])
@login_required
def modify_info():
    pwd_form = form.PasswordModifyForm()
    user_modify_form = form.UserModifyForm()
    user_modify_form.name.data = current_user.name
    user_modify_form.email.data = current_user.email
    user_modify_form.stu_id.data = current_user.stu_id
    user_modify_form.phone.data = current_user.phone
    user_modify_form.motto.data = current_user.remark
    user_modify_form.school.data = current_user.school
    user_modify_form.situation.data = current_user.situation
    pwd_form.username.data = current_user.username
    return render_template('modify_info.html', user=current_user, user_modify_form=user_modify_form, pwd_form=pwd_form)


@profile.route('/profile/post_article', methods=['GET'])
@login_required
def post_article():
    try:
        profile_user = user_server.UserServer.loadUser_or_404(request.args['username'])
    except:
        profile_user = current_user
    solution_form = form.SolutionForm()
    return render_template('post_article.html', user=profile_user, form=solution_form)

@profile.route('/profile/edit_article', methods=['GET'])
@login_required
def edit_article():
    try:
        one = article_server.get_one(request.args['p'])
        if one.user != current_user and current_user.rights == 0:
            raise Exception(u"你没有权限修改该文章")
    except :
        return redirect(url_for('main.index'))
    solution_form = form.SolutionForm()
    if one:
        solution_form.sid.data = one.id
        solution_form.title.data = one.title
        solution_form.shortcut.data = one.shortcut
        solution_form.content.data = one.content
        tags = []
        for tag in one.tags:
            tags.append(tag.__repr__())
        solution_form.tags.data = tags
        solution_form.problem_oj_name.data = one.problem_oj_name
        solution_form.problem_pid.data = one.problem_pid
    return render_template('post_article.html', user=current_user, form=solution_form)