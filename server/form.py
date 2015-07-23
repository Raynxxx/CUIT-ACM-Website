# coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms import BooleanField, SubmitField, RadioField, IntegerField, TextAreaField, FileField
from wtforms import SelectField
from wtforms import Field, widgets
import wtforms.validators as validators
from config import OJ_MAP, SCHOOL_MAP


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

class UserModifyForm(Form):
    name = StringField('Name',validators=[validators.DataRequired()])
    stu_id = StringField('stu_id', validators=[validators.Optional(), validators.Length(min=1, max=20)])
    email = StringField('Email', validators=[validators.Optional(), validators.Length(min=1, max=64), validators.Email()])
    phone = StringField('Phone', validators=[validators.Optional(),validators.Regexp('\d{6,12}', flags=0)])
    school = SelectField('school', validators=[validators.DataRequired()],
                         choices=[(school, SCHOOL_MAP[school]) for school in SCHOOL_MAP],
                         default='cuit')
    situation = StringField('Situation', validators=[validators.Optional()])
    motto = StringField('Motto', validators=[validators.Optional()])
    submit = SubmitField(u'提交')

class PasswordModifyForm(Form):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=1, max=24)])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=6, max=24),
                            validators.EqualTo('password2',message='Passwords must match.')])
    password2 = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=6, max=24)])
    submit = SubmitField(u'提交')


class AccountForm(Form):
    nickname = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=1, max=24),
                    validators.Regexp('^[A-Za-z][A-Za-z0-9_.]*$', flags=0,
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
    shortcut = TextAreaField(u'摘要', validators=[validators.DataRequired()])
    content = TextAreaField(u'正文', validators=[validators.DataRequired()])
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