# encoding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class MTUserLoginForm(Form):
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField(u'密码', validators=[DataRequired(), Length(6, 32)])
    submit = SubmitField(u'登录')


class MTUserPwdForm(Form):
    old_pwd = PasswordField(u'原密码', validators=[DataRequired(), Length(6, 32)])
    new_pwd = PasswordField(u'新密码', validators=[DataRequired(), Length(6, 32)])
    repeat_pwd = PasswordField(u'重复新密码', validators=[DataRequired(), Length(6, 32), EqualTo('new_pwd')])
    submit = SubmitField(u'修改密码')


class MTUserBaseProfileForm(Form):
    name = StringField(u'姓名', validators=[DataRequired()])
    sex = SelectField(u'性别', choices=[(u'男', u'男'), (u'女', u'女')], default=u'男')
    nation = SelectField(u'民族', choices=[(u'汉族', u'汉族'), (u'壮族', u'壮族'), (u'满族', u'满族')], validators=[DataRequired()])
    birthday = DateField(u'出生日期', validators=[DataRequired()])
    email = StringField(u'电子邮箱', validators=[DataRequired(), Email()])
    phone = StringField(u'电话号码')
    blood_type = SelectField(u'血型', choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O'), (u'其他', u'其他')])
    health = StringField(u'健康状况')
    commit = TextAreaField(u'备注')
    submit = SubmitField(u'提交修改')
    bases = {'name', 'sex', 'nation', 'birthday', 'email', 'phone', 'blood_type', 'health', 'commit'}
    extends = set()

    @classmethod
    def add_extend(cls, name, item):
        cls.extends.add(name)
        setattr(cls, name, item)
        return cls