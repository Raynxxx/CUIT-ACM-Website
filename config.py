# coding=utf-8
#The database URI that should be used for the connection.
#fomate: dialect+driver://username:password@host:port/database
#mysql format : mysql://scott:tiger@localhost/database_name
SQLALCHEMY_DATABASE_URI = 'mysql://root:63005610@localhost/cuit_acm'

#A dictionary that maps bind keys to SQLAlchemy connection URIs.
SQLALCHEMY_BINDS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = True

ADMIN = ['Rayn', 'dreameracm']

SCHOOL_MAP = {
    'cuit': u'成都信息工程大学'
}

SCHOOL_COLLEGE_MAP = {
   '0': u"软件工程学院",
   '1': u"计算机学院",
   '2': u"信息安全工程学院",
   '3': u"电子工程学院",
   '4': u"通信工程学院",
   '5': u"应用数学学院",
   '6': u"资源环境学院",
   '7': u"光电技术学院",
   '8': u"控制工程学院",
   '9': u"大气科学学院",
   '10':u"外国语学院",
   '11':u"管理学院",
   '12':u"政治学院",
   '13':u"文化艺术学院",
   '14':u"统计学院",
   '15':u"商学院",
   '16':u"物流学院" ,
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
    'zoj': 'ZOJ',
    'bnu': 'BNU',
    'vj': 'Virtual Judge',
}



CSRF_ENABLED = True
import os.path
BRAND_CONFIG_DEST = os.path.split(os.path.realpath(__file__))[0] + '/brand.ini'
UPLOADED_RESOURCE_DEST = os.path.split(os.path.realpath(__file__))[0] + '/upload/'
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
RESOURCE_MANAGE_PER_PAGE = 10
SITUATION_PER_PAGE = 25
RANK_TABLE_PER_PAGE = 15


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
MAIL_DEBUG = True


#mail template
APPLY_ACCEPT_MAIL = {
    'subject' : u"CUIT ACM Team 申请准许通过",
    'body' : u'''
{name}，非常欢迎你加入我们的团队：

    1、加新生群 392397904 (CUIT ACM/ICPC FM)，记得改下备注哦，格式 “学院年级-姓名”，例如“软工151-XX“；

    2、完成ACM校队官网上的（http://acm.cuit.edu.cn）的新生训练计划；

    3、遇到不懂的问题可以多在群里吼吼，有各种强的师兄师姐热心解答哦；

    4、如果有空的话可以关注各大OJ近期比赛汇总（ACM校队官网首页可以查到），多参加下新生赛，练练手。

                                                    CUIT ACM/ICPC Team
'''
}

APPLY_REJECT_MAIL = {
    'subject' : u"CUIT ACM Team 申请拒绝通过",
    'body' : u'''
{name}，非常感谢你的申请，但不幸运的是我们不能通过你的申请，可能是由于你的申请信息填写
有误，你可以访问 http://acm.cuit.edu.cn/join_us 尝试重新申请。

                                                    CUIT ACM/ICPC Team
'''
}

