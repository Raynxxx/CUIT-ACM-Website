# coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms import BooleanField, SubmitField, RadioField, IntegerField, \
    TextAreaField, FileField, DateField, SelectMultipleField
from wtforms import SelectField
from wtforms import Field, widgets
import wtforms.validators as validators
from config import OJ_MAP, SCHOOL_MAP ,HONOR_LEVEL_MAP


class LoginForm(Form):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=1, max=24)])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=6, max=24)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField(u'登录')


class RegisterForm(Form):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=1, max=24),
                    validators.Regexp('^[A-Za-z][A-Za-z0-9_.]*$', flags=0,
                    message='Username must have only letters, numbers, dots or underscores')])
    name = StringField('Name',validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=6, max=24),
                    validators.EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[validators.DataRequired()])
    stu_id = StringField('stu_id', validators=[validators.Optional(), validators.Length(min=1, max=20)])
    phone = StringField('stu_id', validators=[validators.Optional(), validators.Length(min=1, max=15)])
    school = SelectField('school', validators=[validators.DataRequired()],
                         choices=[(school, SCHOOL_MAP[school]) for school in SCHOOL_MAP],
                         default='cuit')
    gender = RadioField('Gender', choices=[('1', u'男'), ('0', u'女')], coerce=str, default=1)
    email = StringField('Email', validators=[validators.DataRequired(), validators.Length(min=1, max=64), validators.Email()])
    submit = SubmitField(u'注册')

class MultiRegisterForm(Form):
    user_info = TextAreaField(u'用户信息', validators=[validators.DataRequired()])
    submit = SubmitField(u'提交')


class UserModifyForm(Form):
    id = IntegerField('id', validators=[validators.optional()])
    name = StringField('Name', validators=[validators.DataRequired()])
    stu_id = StringField('stu_id', validators=[validators.Optional(), validators.Length(min=1, max=20)])
    email = StringField('Email', validators=[validators.Optional(), validators.Length(min=1, max=64), validators.Email()])
    phone = StringField('Phone', validators=[validators.Optional(),validators.Regexp('\d{6,12}', flags=0)])
    school = SelectField('school', validators=[validators.DataRequired()],
                         choices=[(school, SCHOOL_MAP[school]) for school in SCHOOL_MAP],
                         default='cuit')
    motto = StringField('Motto', validators=[validators.Optional()])
    situation = StringField('Situation', validators=[validators.Optional()])
    active = RadioField('Active', choices=[('1', u'训练 ing'), ('0', u'退役狗')], coerce=str, default=1)
    gender = RadioField('Gender', choices=[('1', u'男'), ('0', u'女')], coerce=str, default=1)
    submit = SubmitField(u'提交')


class PasswordModifyForm(Form):
    id = IntegerField('id', validators=[validators.optional()])
    password = PasswordField('origin password', validators=[validators.DataRequired(), validators.Length(min=6, max=24)])
    new_password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=6, max=24),
                            validators.EqualTo('new_password2',message='Passwords must match.')])
    new_password2 = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=6, max=24)])
    submit = SubmitField(u'提交')


class AccountForm(Form):
    nickname = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=1, max=24),
                    validators.Regexp('^[A-Za-z0-9_.][A-Za-z0-9_.]*$', flags=0,
                    message='Username must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=3, max=24)])
    oj_name = SelectField('OJ', validators=[validators.DataRequired()],
                          choices=[(oj, OJ_MAP[oj]) for oj in OJ_MAP],
                          default='bnu')
    submit = SubmitField(u'提交')


class TagListField(Field):
    widget = widgets.TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []


class SolutionForm(Form):
    sid = IntegerField('id',validators=[validators.optional()],default=-1)
    title = StringField(u'标题', validators=[validators.DataRequired()])
    shortcut = TextAreaField(u'摘要', validators=[validators.DataRequired()])
    content = TextAreaField(u'正文', validators=[validators.DataRequired()])
    problem_oj_name = SelectField('OJ',
                          choices=[(oj, OJ_MAP[oj]) for oj in OJ_MAP],
                          default='bnu')
    problem_pid = StringField('PID', validators=[validators.optional(), validators.Regexp('^[A-Z0-9]*$', flags=0)])
    tags = TagListField(u'标签', validators=[validators.DataRequired()])
    submit = SubmitField(u'提交')


class NewsForm(Form):
    sid = IntegerField('id',validators=[validators.optional()],default=-1)
    title = StringField(u'标题', validators=[validators.DataRequired()])
    url = StringField(u'url', validators=[validators.DataRequired(), validators.Regexp('^[a-zA-Z0-9-_&+%]*$', flags=0)])
    content = TextAreaField(u'正文', validators=[validators.DataRequired(),validators.Length(min=10)])
    is_top = BooleanField(u'置顶')
    tags = TagListField(u'标签', validators=[validators.DataRequired()])
    submit = SubmitField(u'提交')


class BookForm(Form):
    id = IntegerField('id',validators=[validators.optional()],default=-1)
    status = IntegerField('status',validators=[validators.optional()],default=0)
    name = StringField(u'name', validators=[validators.DataRequired()])
    shortcut = StringField(u'icon', validators=[validators.Optional()])
    upload = FileField(u'file')
    introduce = TextAreaField(u'introduce', validators=[validators.DataRequired()])
    isbn = StringField(u'标题', validators=[validators.DataRequired()])
    submit = SubmitField(u'提交')


class FileUploadForm(Form):
    name = StringField(u'name', validators=[validators.DataRequired(), validators.Length(min=1, max=48)])
    description = TextAreaField(u'description', validators=[validators.Optional()])
    level = RadioField('level', choices=[('0', u'公开'), ('1', u'共享'), ('2', u'私有')], coerce=str, default=2)
    usage = RadioField('usage',choices=[('0', u'图书资源'), ('1', u'荣誉资源'), ('2', u'新闻资源'),
                                        ('3',u'题解资源'), ('4',u'其他资源')], coerce=str, default=2)
    upload = FileField(u'file')
    submit = SubmitField(u'提交')


class FileInfoForm(Form):
    id = IntegerField('id',validators=[validators.optional()],default=-1)
    name = StringField(u'name', validators=[validators.DataRequired(), validators.Length(min=1, max=48)])
    description = TextAreaField(u'description', validators=[validators.Optional()])
    level = RadioField('level', choices=[('0', u'公开'), ('1', u'内部共享'), ('2', u'私有')], coerce=str, default=2)
    usage = RadioField('usage',choices=[('0', u'图书资源'), ('1', u'荣誉资源'), ('2', u'新闻资源'),
                                        ('3',u'题解资源'), ('4',u'其他资源')], coerce=str, default=4)
    submit = SubmitField(u'提交')


class HonorForm(Form):
    id = IntegerField('id',validators=[validators.optional()],default=-1)
    contest_name = StringField(u'contest_name', validators=[validators.DataRequired(), validators.Length(min=1, max=48)])
    contest_level = SelectField('contest_level', validators=[validators.DataRequired()],
                         choices=[(str(honor), HONOR_LEVEL_MAP[honor]) for honor in HONOR_LEVEL_MAP],
                         default='0')
    acquire_time = DateField('acquire_time', format='%Y/%m/%d')
    type = RadioField('type', choices=[('single', u'单人'), ('group', u'组队')], coerce=str, default='single')
    introduce = TextAreaField(u'introduce', validators=[validators.Optional()])
    users = SelectMultipleField(u'users', validators=[validators.DataRequired()])
    submit = SubmitField(u'提交')