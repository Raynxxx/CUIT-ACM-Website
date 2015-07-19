# coding=utf-8
from __init__ import *
from config import OJ_MAP

class UserServer():
    def __init__(self, user):
        self.user = user

    def get_account_info(self):
        have = []
        not_have = []
        if self.user.account:
            accounts = self.user.account.all()
            for account in accounts:
                have.append(account.oj_name)
        for oj_name in OJ_MAP:
            if oj_name not in have:
                not_have.append(oj_name)
        return {'have': have, 'not_have': not_have}

    def get_general_info(self, oj_name):
        if not self.user.account:
            return None
        account = self.user.account.filter_by(oj_name=oj_name).first()
        if account:
            ret = account.get_problem_count()
            ret['last_update_time'] = account.last_update_time
            return ret
        return None

    @staticmethod
    def addUser(userInfo):
        has = User.query.filter_by(username=userInfo.username.data).first()
        if has:
            return "该用户名已经存在"
        gender = True if userInfo.gender.data == '1' else False
        user = User(username=userInfo.username.data,
                    name=userInfo.name.data,
                    password=userInfo.password.data,
                    stu_id=userInfo.stu_id.data,
                    gender=gender,
                    email=userInfo.email.data)
        user.save()

    @staticmethod
    def loadUser_or_404(username):
        return User.query.filter_by(username=username).first_or_404()

    @staticmethod
    def loadUser(username):
        return User.query.filter_by(username=username).first()

    def get_statistic(self):
        stat = dict()
        stat['total_submit'] = self.user.submit.count()
        now = datetime.datetime.now()
        permit_date = now - datetime.timedelta(days=now.weekday())
        permit_date = permit_date.replace(hour=0, minute=0, second=0)
        stat['weekly_submit'] = self.user.submit.filter(Submit.submit_time > permit_date).count()
        return stat

    @staticmethod
    def get_user_list(offset=0, limit=20):
        users = User.query.offset(offset).limit(limit)
        return users

    def modify_password(self, pwdInfo):
        has = self.loadUser(pwdInfo.username.data)
        if not has:
            return u"不存在该用户"
        if (not self.user.is_admin) and self.user != has:
            return u"你没有权限修改密码"
        if pwdInfo.password.data != pwdInfo.verifypassword.data:
            return u"两次输入的密码不同"
        has.password = pwdInfo.password.data
        has.save()
        return u"修改密码成功"

    def modify_info(self, userInfo):
        self.user.email = userInfo.email.data
        self.user.stu_id = userInfo.stu_id.data
        self.user.name = userInfo.name.data
        self.user.school = userInfo.school.data
        self.user.situation = userInfo.situation.data
        self.user.phone = userInfo.phone.data
        self.user.remark = userInfo.motto.data
        self.user.save()





