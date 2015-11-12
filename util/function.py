#
# public function used by CUIT web site
#
from  threading import  Thread
from flask.ext.mail import Message
import config

def user_rank_color(score):
    if score in xrange(0,1000):
        return "#24e5bf"
    elif score in xrange(1000,1500):
        return "#f2cf2e"
    else :
        return "#fd8321"

def submit_result_color(res):
    result = res.lower()
    if result == 'ok' or result == 'accepted':
        return 'blue'
    else :
        return 'red'


problem_page_mapper = {
    'hdu': 'http://acm.hdu.edu.cn/showproblem.php?pid={pid}',
    'poj': 'http://poj.org/problem?id={pid}',
    'zoj': 'http://acm.zju.edu.cn/onlinejudge/showProblem.do?problemCode={pid}',
    'bnu': 'http://acm.bnu.edu.cn/v3/problem_show.php?pid={pid}',
    'vj': 'http://acm.hust.edu.cn/vjudge/problem/viewProblem.action?id={pid}',
}

def submit_problem_page(oj_name, pid):
    if oj_name in problem_page_mapper:
        return "<a href='{url}'>{pid}</a>".format(url = problem_page_mapper[oj_name].format(pid=pid), pid = pid)
    return str(pid)


def async(func):
    def wrapper(*args, **kwargs):
        func_thread = Thread(target = func, args = args, kwargs = kwargs)
        func_thread.start()
    return wrapper

#
# @brief: send ail
# @allowed user: all
#
def send_mail(sender, msg):
    sender.send(msg)

@async
def reply_of_apply(sender, user, app, opt):
    if opt == 'accept':
        template_mail = config.APPLY_ACCEPT_MAIL
    else:
        template_mail = config.APPLY_REJECT_MAIL
    title = template_mail['title'].format(name=user['name'])
    content = template_mail['body']
    recipient = user['email']
    with app:
        msg = Message(title, recipients=[recipient], body=content)
        send_mail(sender, msg)