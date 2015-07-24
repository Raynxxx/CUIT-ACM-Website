# coding=utf-8
from __init__ import *
from server import user_server, general, article_server, form
from config import OJ_MAP
import util
#
# @blueprint: profile
# @created: 2015/06/22
# @author: Z2Y
#
profile = blueprints.Blueprint('profile', __name__, template_folder='../templates/profile')

#
# @brief: the profile page
# @route: /profile
# @accepted methods: [get]
# @allowed user: all
#
@profile.route('/profile')
@login_required
def index():
    try:
        profile_user = user_server.get_by_username_or_404(request.args['username'])
    except:
        profile_user = current_user
    statistic = user_server.get_statistic(profile_user)
    user_modify_form = form.UserModifyForm()

    user_modify_form.id.data = profile_user.id
    user_modify_form.name.data = profile_user.name
    user_modify_form.stu_id.data = profile_user.stu_id
    user_modify_form.email.data = profile_user.email
    user_modify_form.phone.data = profile_user.phone
    user_modify_form.motto.data = profile_user.remark
    user_modify_form.situation.data = profile_user.situation
    user_modify_form.school.data = profile_user.school
    user_modify_form.gender.data = '1' if profile_user.gender else '0'
    user_modify_form.active.data = '1' if profile_user.active else '0'
    return render_template('index.html',
                           title=u'你的主页',
                           user = profile_user,
                           user_modify_form = user_modify_form,
                           stat = statistic,
                           school_mapper = SCHOOL_MAP)

#
# @brief: the OJ account management page
# @route: /profile/manage_account
# @accepted methods: [get]
# @allowed user: self, admin and coach
#
@profile.route('/profile/manage_account', methods=['GET'])
@login_required
def manage_account():
    try:
        profile_user = user_server.get_by_username_or_404(request.args['username'])
    except:
        profile_user = current_user
    if current_user != profile_user and (not current_user.is_admin and not current_user.is_coach_of(profile_user)):
        return u"没有权限"
    account_form = form.AccountForm()
    return render_template('manage_account.html',
                           title = u'OJ账号管理',
                           form=account_form,
                           user=profile_user)


@profile.route('/profile/update_account', methods=['GET'])
@login_required
def update_account():
    try:
        profile_user = user_server.get_by_username_or_404(request.args['username'])
    except:
        profile_user = current_user
    if current_user == profile_user or current_user.is_admin or current_user.is_coach:
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
    solution_form = form.SolutionForm()
    return render_template('post_article.html', user=current_user, form=solution_form)


@profile.route('/profile/edit_article', methods=['GET'])
@login_required
def edit_article():
    try:
        one = article_server.get_by_id(request.args['p'])
        if one.user != current_user and (not current_user.is_admin and not current_user.is_coach):
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