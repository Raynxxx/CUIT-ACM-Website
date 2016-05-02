# coding=utf-8
from __init__ import *
from werkzeug.exceptions import NotFound
from server import user_server, general, article_server, form, news_server, resource_server, honor_server
from dao.dbBase import User
from dao.dbResource import ResourceLevel
from dao import dbCompetition, dbPlayer
from util import function
import config, json


main = blueprints.Blueprint('main', __name__)


#
# @brief: login page
# @route: /login
# @accepted methods: [get, post]
# @allowed user: all
#
@main.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.news_list'))
    login_form = form.LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None:
            flash(u'用户不存在!')
        elif not user.verify_password(login_form.password.data):
            flash(u'密码错误!')
        elif user.is_apply:
            flash(u'用户未通过审核')
        else:
            login_user(user, remember=login_form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
    else:
        pass
    return render_template('index/login.html',
                           title = u'登录',
                           login_form = login_form)


#
# @brief: join us page
# @route: /join_us
# @accepted methods: [get, post]
# @allowed user: all
#
@main.route('/join_us', methods=["GET", "POST"])
def join_us():
    join_form = form.RegisterForm()
    if join_form.validate_on_submit():
        try:
            ret = user_server.create_user(join_form, 8)
            if ret == 'OK':
                #send_register_success(join_form.email.data, _app_ctx_stack.top, join_form)
                flash(u"提交申请成功")
            else:
                flash(u"提交申请失败: " + ret)
        except Exception, e:
            flash(u"提交申请失败: " + e.message)
    else:
        for errors in join_form.errors.values():
            for error in  errors:
                flash(error)
    return render_template('index/register.html',
                           title = u'加入我们',
                           join_form = join_form)


#
# @brief: logout action, to redirect login page
# @route: /login
# @accepted methods: [get, post]
# @allowed user: all
#
@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    #flash(u'你已下线本系统')
    return redirect(url_for('main.index'))


#
# @brief: index page
# @route: /index
# @accepted methods: [get, post]
# @allowed user: all
#
@main.route('/')
@main.route('/index')
def index():
    recent_news = news_server.get_recent(sortTop=True)
    from dao.dbResource import Resource, ResourceUsage
    posters = Resource.query.filter(Resource.usage == ResourceUsage.POSTER_RES).all()
    json_file = open(RECENT_CONTEST_JSON, 'r').read()
    json_contests = json.loads(json_file)
    recent_contests = [[contest['name'], contest['link']] for contest in json_contests]
    from datetime import date
    cur_year = date.today().year
    return render_template('index/index.html',
                           title = 'CUIT ACM Team',
                           posters = posters,
                           recent_news = recent_news,
                           recent_contests = recent_contests[:5],
                           recommend_site = config.RECOMMEND_SITE,
                           file_url = resource_server.file_url,
                           cur_year = cur_year)


#
# @brief: page for news list
# @route: /news_list
# @accepted methods: [get]
# @allowed user: all
#
@main.route('/news_list', methods=['GET'])
@main.route('/news_list/<page>', methods=['GET'])
def news_list(page = 0):
    limit = config.NEWS_PER_PAGE
    offset = int(page) * limit
    news_server.get_archive()
    news = news_server.get_list(offset, limit)
    recent_news = news_server.get_recent()
    tags = news_server.get_all_tags()
    sum = news_server.get_count()
    return render_template('index/news_list.html',
                          title = u'新闻',
                          news = news, tags = tags,
                          recent_news = recent_news,
                          page = int(page),
                          sum = sum, limit = limit)


#
# @brief: page for one news
# @route: /news
# @accepted methods: [get]
# @allowed user: all
#
@main.route('/news')
@main.route('/news/<url>', methods = ['GET'])
def news(url=None):
    try:
        if url:
            one_news = news_server.get_by_url(url)
        else:
            sid = request.args['p']
            one_news = news_server.get_by_id(sid)
        recent_news = news_server.get_recent()
        tags = news_server.get_all_tags()
    except Exception, e:
        return redirect(url_for('main.news_list'))
    return render_template('index/news.html',
                           title=one_news.title,
                           one=one_news,
                           recent_news=recent_news,
                           tags=tags)


#
# @brief: page for archive of news tag
# @route: /news/archive/<tag>
# @accepted methods: [get]
# @allowed user: all
#
@main.route('/news/archive', methods = ['GET'])
@main.route('/news/archive/<tag>', methods = ['GET'])
def news_archive(tag=None):
    if tag:
        title = u'Archive ' + tag
        archives = news_server.get_archive_by_tag(tag)
    else:
        title = u'Archive'
        archives = news_server.get_archive()
    return render_template('index/archive.html',
                           title = title,
                           archives = archives)


#
# @brief: page for rank list
# @route: /ranklist
# @accepted methods: [get]
# @allowed user: all
#
@main.route('/rank_list', methods = ['GET'])
@login_required
def rank_list():
    weekly_rank_list = general.get_weekly_info(False)[0:10]
    last_week_rank = general.get_weekly_info(True)[0:10]
    return render_template('index/rank_list.html',
                           title = u'查水表',
                           weekly_rank = weekly_rank_list,
                           last_week_rank = last_week_rank,
                           RANK_TABLE_PER_PAGE = config.RANK_TABLE_PER_PAGE)


#
# @brief: page for all status
# @route: /ranklist
# @accepted methods: [get]
# @allowed user: all
#
@main.route('/status', methods = ['GET'])
@login_required
def status():
    return render_template('index/status.html',
                           title = u'最近提交')


#
# @brief: page for view code of one submit
# @route: /viewcode/<oj_name>/<run_id>
# @accepted methods: [get]
# @allowed user: all
#
@main.route('/viewcode/<oj_name>/<run_id>', methods = ['GET'])
@login_required
def view_code(oj_name, run_id):
    submit = general.get_submit(oj_name, run_id)
    if not submit:
        flash(u'读取代码失败!')
        return redirect(url_for('main.status'))
    return render_template('index/viewcode.html',
                           title = 'Show Code',
                           submit = submit,
                           oj_mapper = OJ_MAP)


#
# @brief: page for all article
# @route: /article_list
# @accepted methods: [get]
# @allowed user: all
#
@main.route('/article_list/', methods=['GET'])
@main.route('/article_list', methods=['GET'])
@main.route('/article_list/<page>', methods=['GET'])
@login_required
def article_list(page=0):
    limit = config.ARTICLE_PER_PAGE
    query_type = request.args.get('query_type')
    keyword = request.args.get('keyword')
    keyword = keyword if keyword else ''
    sum = article_server.get_count(query_type=query_type, keyword = keyword)
    try :
        offset = int(page) * limit
        tags = article_server.get_all_tags()
        articles = article_server.get_list(offset, limit, query_type=query_type, keyword = keyword)
        recent_articles = article_server.get_recent()

        return render_template('index/article_list.html',
                               title = u'解题报告',
                               articles = articles,
                               tags = tags,
                               recent_articles = recent_articles,
                               page = int(page),
                               sum = sum, limit = limit, query_type = query_type, keyword = keyword)
    except:
        return redirect(url_for("main.article_list"))


#
# @brief: page for one article
# @route: /article
# @accepted methods: [get]
# @allowed user: all
#
@main.route('/article', methods=['GET'])
@login_required
def article():
    try:
        pid = request.args['p']
        one = article_server.get_by_id(pid)
        recent_articles = article_server.get_recent()
        return render_template('index/article.html',
                               title = one.title,
                               one = one,
                               recent_articles = recent_articles)
    except:
        return redirect(url_for('main.article_list'))


#
# @brief: route to fitch resource
# @route: /upload/resource/<path:name>
# @accepted methods: [all]
# @allowed user: all
#
@main.route('/upload/resource/<path:name>', methods=['GET'])
def resource(name):
    if name.startswith('cache/'):
        return send_from_directory(config.UPLOADED_RESOURCE_DEST, name, as_attachment=True,
                                   attachment_filename=name.encode('utf-8'))
    rs = resource_server.get_by_filename(name)
    if rs.level ==  ResourceLevel.PUBLIC:
        return send_from_directory(config.UPLOADED_RESOURCE_DEST, rs.filename, as_attachment=True,
                                   attachment_filename=rs.filename.encode('utf-8'))
    elif rs.level == ResourceLevel.SHARED:
        if not current_user.is_authenticated():
            abort(403)
        return send_from_directory(config.UPLOADED_RESOURCE_DEST, rs.filename, as_attachment=True,
                                   attachment_filename=rs.filename.encode('utf-8'))
    else:
        if not current_user.is_authenticated():
            abort(403)
        elif current_user.is_admin or current_user.is_coach_of(rs.user):
            return send_from_directory(config.UPLOADED_RESOURCE_DEST, rs.filename, as_attachment=True,
                                       attachment_filename=rs.filename.encode('utf-8'))
        else:
            abort(403)


#
# @brief: page for honor wall
# @route: /honor_wall
# @accepted methods: [get]
# @allowed user: all
#
@main.route("/honor_wall", methods = ['GET'])
def honor_wall():
    query_type = request.args.get('query_type')
    keyword = request.args.get('keyword')
    honor_wall = honor_server.get_honor_wall_by_year(query_type, keyword)
    return render_template('index/honor_wall.html',
                           title = u'荣誉墙',
                           honor_wall = honor_wall,
                           HONOR_LEVEL_MAP = HONOR_LEVEL_MAP,
                           file_url = resource_server.file_url)

#
# @brief: page for honor
# @route: /honor/honor_id
# @accepted methods: [get]
# @allowed user: all
#
@main.route("/honor", methods = ['GET'])
@main.route("/honor/<honor_id>", methods = ['GET'])
def honor(honor_id=None):
    if not honor_id:
        return redirect(url_for('main.honor_wall'))
    honor = honor_server.get_by_id(honor_id)
    return render_template('index/honor.html',
                           title = u'荣誉',
                           honor = honor,
                           HONOR_LEVEL_MAP = HONOR_LEVEL_MAP)


#
# @brief: page for members situation
# @route: /members
# @accepted methods: [get]
# @allowed user: all
#
@main.route("/members", methods=['GET'])
def members():
    return render_template('index/members.html',
                           title = u'队员去向',
                           SITUATION_PER_PAGE = config.SITUATION_PER_PAGE)


#
# @brief: page for join competition
# @route: /competition/join/<year>
# @accepted methods: [get, post]
# @allowed user: all
#
@main.route('/competition/join', methods=['GET', 'POST'])
@main.route('/competition/join/<year>', methods=['GET', 'POST'])
def competition_join(year=None):
    if not year:
        from datetime import datetime
        year = datetime.now().year
    competition_of_year = dbCompetition.get_by_year(year)
    player_form = form.PlayerForm()
    if request.method == 'POST' and player_form.validate_on_submit():
        has = dbPlayer.get_by_stu_and_name(player_form.stu_id.data,
                                           player_form.name.data)
        if not has:
            feedback = dbPlayer.create_player(player_form)
            if feedback[0] != 'OK':
                flash(feedback[0])
            else:
                feedback = dbCompetition.create_join(competition_of_year, feedback[1])
                flash(u'报名成功') if feedback == 'OK' else flash(feedback)
        else:
            feedback = dbCompetition.create_join(competition_of_year, has)
            flash(u'报名成功') if feedback == 'OK' else flash(feedback)
    else:
        for errors in player_form.errors.values():
            for error in  errors:
                flash(error)
    return render_template('index/competition_join.html',
                           title = u'校赛报名',
                           cur_year = year,
                           competition_of_year = competition_of_year,
                           player_form = player_form)
