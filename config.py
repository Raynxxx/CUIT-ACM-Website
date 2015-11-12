# coding=utf-8
#The database URI that should be used for the connection.
#fomate: dialect+driver://username:password@host:port/database
#mysql format : mysql://scott:tiger@localhost/database_name
SQLALCHEMY_DATABASE_URI = 'mysql://root:63005610@localhost/cuit_acm'

#A dictionary that maps bind keys to SQLAlchemy connection URIs.
SQLALCHEMY_BINDS = {}

ADMIN = ['Rayn', 'dreameracm']

SCHOOL_MAP = {
    'cuit': u'成都信息工程大学',
    'scu': u'四川大学'
}

SCHOOL_COLLEGE_MAP = {
   0: u"软件工程学院",
   1: u"计算机学院",
   2: u"信息安全工程学院",
   3: u"电子工程学院",
   4: u"通信工程学院",
   5: u"应用数学学院",
   6: u"资源环境学院",
   7: u"光电技术学院",
   8: u"控制工程学院",
   9: u"大气科学学院",
   10:u"外国语学院",
   11:u"管理学院",
   12:u"政治学院",
   13:u"文化艺术学院",
   14:u"统计学院",
   15:u"商学院",
   16:u"物流学院" ,
}

HONOR_LEVEL_MAP = {
    0: u'区域赛金奖',
    1: u'区域赛银奖',
    2: u'区域赛铜奖',
    3: u'区域赛优胜奖',
    4: u'省赛一等奖',
    5: u'省赛二等奖',
    6: u'省赛三等奖',
    7: u'省赛优胜奖',
    8: u'校赛特等奖',
    9: u'校赛一等奖',
    10: u'校赛二等奖',
    11: u'校赛三等奖',
}

OJ_MAP = {
    'hdu': 'HDU',
    'cf': 'Codeforces',
    'bc': 'BestCoder',
    'poj': 'POJ',
    'uva': 'UVA',
    'zoj': 'ZOJ',
    'bnu': 'BNU',
    'vj': 'Virtual Judge',
}



CSRF_ENABLED = True
import os.path
BRAND_CONFIG_DEST = os.path.split(os.path.realpath(__file__))[0] + '/brand.ini'
UPLOADED_RESOURCE_DEST = os.path.split(os.path.realpath(__file__))[0] + '/static/resource/'
UPLOADED_RESOURCE_URL = '/upload/resource/'
IMAGE_FILE_PATH = 'static/image/bookimg/'
SECRET_KEY = 'a very hard string'
from datetime import timedelta
REMEMBER_COOKIE_DURATION = timedelta(days=1)

## some config for front end
NEWS_PER_PAGE = 10
ARTICLE_PER_PAGE = 5
USER_MANAGE_PER_PAGE = 8
NEWS_MANAGE_PER_PAGE = 8
ARTICLE_MANAGE_PER_PAGE = 8
HONOR_MANAGE_PER_PAGE = 8
RESOURCE_MANAGE_PER_PAGE = 8


#index information
RECENT_CONTEST_JSON = os.path.split(os.path.realpath(__file__))[0] + '/static/json/contests.json'

RECOMMEND_SITE = {
    u'ACM/ICPC信息站' : 'http://acmicpc.info',
    'BNU OJ' : 'http://acm.bnu.edu.cn',
    u'ACM-ICPC官网' : 'https://icpc.baylor.edu/',
    'BestCoder': 'http://bestcoder.acmcoder.com/',
    u'CUIT学校主页': 'http://www.cuit.edu.cn'
}


#mail config
MAIL_SERVER = 'mail.cuit.edu.cn'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "acmicpc@cuit.edu.cn"
MAIL_PASSWORD = "xbnahn"
MAIL_DEFAULT_SENDER = "acmicpc@cuit.edu.cn"
MAIL_DEBUG = False


#mail template
APPLY_ACCEPT_MAIL = {
    'title' : u"{name}，非常高兴你积极的报名。我们非常欢迎你的参与",
    'body' : u'''先做几件事：

1、加新生群34117625，记得改下名字哦，格式“学院-年级-姓名”；

2、上acm.bnu.edu.cn（或219.224.30.70），把Problem前100题都做了（就是1000到1099），其中可能会遇到比较难的题，可以适当的放弃；

3、简单说一下训练安排：因为临近考试周，训练部分暂停，寒假或者下学期开学后会统一组织训练，这个会在群里通知的。当然，如果时间充足，bnuoj上的新手题也做完了，请及时跟我们联系。遇到不懂的问题可以多在群里吼吼，有各种强的师兄师姐热心解答哦；

4、近期各大OJ上比赛比较多，如果有空的话可以关注各大OJ近期比赛汇总（http://acmicpc.info/archives/224），多参加下新生赛，练练手；

                                              CUIT ACM/ICPC Team
'''
}

APPLY_REJECT_MAIL = {
    'title' : u"{name} reject!",
    'body' : u"reject!"
}

