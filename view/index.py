# coding=utf-8
from __init__ import *
from server import user_server, general, article_server, form, book_server, news_server
from dao.dbBase import User


main = blueprints.Blueprint('main', __name__)

@main.route('/login', methods=["GET", "POST"])
def login():
    login_form = form.LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None:
            flash(u'用户不存在!')
        elif not user.verify_password(login_form.password.data):
            flash(u'密码错误!')
        else:
            login_user(user, remember=login_form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('index/login.html', form=login_form)

@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))

@main.route('/')
@main.route('/index')
def index():
    news_server.get_archive()
    news = news_server.get()
    return render_template('index/index.html', news=news)

@main.route('/archive')
@main.route('/archive/<tag>')
def archive(tag=None):
    if tag:
        arch = news_server.get_archive_by_tag(tag)
    else:
        arch = news_server.get_archive()
    return render_template('index/archive.html', archive=arch)

@main.route('/aboutus')
def about():
    return redirect(url_for('main.ranklist'))
    #return render_template('index/about.html')

@main.route('/ranklist')
@login_required
def ranklist():
    weekly_rank_list = general.get_weekly_info(False)[0:10]
    last_week_rank = general.get_weekly_info(True)[0:10]
    info_list = general.get_info_list()
    return render_template('index/ranklist.html', weekly_rank=weekly_rank_list, last_rank=last_week_rank, info_list=info_list)

@main.route('/footmark')
@login_required
def footmark():
    return render_template('index/footmark.html')

@main.route('/article_list')
@login_required
def article_list():
    article = article_server.get()
    return render_template('index/article_list.html', article = article)

@main.route('/article')
@login_required
def article():
    try:
        pid = request.args['p']
        one = article_server.get_one(pid)
        return render_template('index/article.html', one=one)
    except:
        return redirect(url_for('main.index'))

@main.route('/news')
@main.route('/news/<url>', methods = ['GET'])
@login_required
def news(url=None):
    try:
        if url:
            one = news_server.get_one_by_url(url)
        else:
            sid = request.args['p']
            one = news_server.get_one(sid)
        return render_template('index/news.html', one=one)
    except :
        return redirect(url_for('main.index'))


@main.route("/book", methods = ['GET'])
@login_required
def book_list():
    status_map = {0:u'可借', 1:u'已借出',2:"超时未归还"}
    books = book_server.list_book()
    return render_template('index/book_list.html', books = books, smap = status_map)

@main.route('/status')
@login_required
def status():
    return render_template('index/status.html', title='Status')

@main.route('/viewcode/<oj_name>/<run_id>')
@login_required
def view_code(oj_name, run_id):
    submit = general.get_submit(oj_name, run_id)
    if not submit:
        flash(u'读取代码失败!')
        return redirect(url_for('status', oj_name=oj_name))
    return render_template('index/viewcode.html', title='Show Code', submit=submit)
