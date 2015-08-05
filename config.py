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

HONOR_LEVEL_MAP = {
    0:u'区域赛金奖',
    1:u'区域赛银奖',
    2:u'区域赛铜奖',
    3:u'区域赛优胜奖',
    4:u'省赛金奖',
    5:u'省赛银奖',
    6:u'省赛铜奖',
    7:u'省赛优胜奖',
    8:u'校赛特等奖',
    9:u'校赛一等奖',
    10:u'校赛二胜奖',
    11:u'校赛三胜奖',

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
UPLOADED_RESOURCE_DEST = os.path.split(os.path.realpath(__file__))[0] + '/static/resource/'
UPLOADED_RESOURCE_URL = '/upload/resource/'
IMAGE_FILE_PATH = 'static/image/bookimg/'
SECRET_KEY = 'a very hard string'
from datetime import timedelta
REMEMBER_COOKIE_DURATION = timedelta(days=1)

## some config for front end
NEWS_PER_PAGE = 5
USER_MANAGE_PER_PAGE = 5
NEWS_MANAGE_PER_PAGE = 5
RESOURCE_MANAGE_PER_PAGE = 8
