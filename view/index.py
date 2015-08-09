# coding=utf-8
from __init__ import *
from werkzeug.exceptions import NotFound
from server import user_server, general, article_server, form, book_server, news_server, resource_server, honor_server
from dao.dbBase import User
from dao.dbResource import ResourceLevel
import config


main = blueprints.Blueprint('main', __name__)

#
# @brief: login page
# @route: /login
# @accepted methods: [get, post]
# @allowed user: all
#
@main.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('main.news_list'))
    login_form = form.LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None:
            flash(u'用户不存在!')
        elif not user.verify_password(login_form.password.data):
            flash(u'密码错误!')
        else:
            login_user(user, remember=login_form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.news_list'))
    return render_template('index/login.html',
                           login_form = login_form)


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
    return render_template('index/index.html',
                           recent_news = news_server.get_recent())


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
        return render_template('index/news.html',
                               title = one_news.title,
                               one = one_news,
                               recent_news = recent_news,
                               tags = tags)
    except Exception, e:
        return redirect(url_for('main.index'))


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
@main.route('/ranklist', methods = ['GET'])
@login_required
def ranklist():
    weekly_rank_list = general.get_weekly_info(False)[0:10]
    last_week_rank = general.get_weekly_info(True)[0:10]
    info_list = general.get_rank_list()
    return render_template('index/ranklist.html',
                           weekly_rank = weekly_rank_list,
                           last_week_rank = last_week_rank,
                           info_list = info_list)


#
# @brief: page for all status
# @route: /ranklist
# @accepted methods: [get]
# @allowed user: all
#
@main.route('/status', methods = ['GET'])
@login_required
def status():
    return render_template('index/status.html', title='Status')


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
@main.route('/article_list', methods=['GET'])
@login_required
def article_list():
    articles = article_server.get_list()
    recent_articles = article_server.get_recent()
    return render_template('index/article_list.html',
                           articles = articles,
                           recent_articles = recent_articles)


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
        return render_template('index/article.html', one=one,
                               recent_articles = recent_articles)
    except:
        return redirect(url_for('main.article_list'))



#
# @brief: page for archive of article tag
# @route: /article/archive/<tag>
# @accepted methods: [get]
# @allowed user: all
#
@main.route('/article/archive', methods=['GET'])
@main.route('/article/archive/<tag>', methods=['GET'])
def article_archive(tag=None):
    if tag:
        archives = article_server.get_archive_by_tag(tag)
    else:
        archives = article_server.get_archive()
    return render_template('index/archive.html', archives=archives)



#
# @brief: route to fitch resource
# @route: /upload/resource/<path:name>
# @accepted methods: [all]
# @allowed user: all
#
@main.route('/upload/resource/<path:name>')
def resource(name):
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
    return render_template('index/honor_wall.html',
                           title = u'荣誉墙',
                           limit = config.HONOR_PER_PAGE,
                           HONOR_LEVEL_MAP = HONOR_LEVEL_MAP)


@main.route('/aboutus')
def about():
    return redirect(url_for('main.ranklist'))
    #return render_template('index/about.html')



@main.route('/footmark')
@login_required
def footmark():
    return render_template('index/footmark.html')


@main.route("/book", methods = ['GET'])
@login_required
def book_list():
    status_map = {0:u'可借', 1:u'已借出',2:"超时未归还"}
    books = book_server.list_book()
    return render_template('index/book_list.html', books = books, smap = status_map)




