from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField, FileField
from wtforms.validators import ValidationError, DataRequired, Length, Email, equal_to
from flask_wtf.file import FileRequired, FileAllowed
from app.models import User


# 表单注册类
class Register(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'),
                                              Length(min=6, max=12, message='用户名不能超过50个字')],
                           render_kw={'placeholder': '请输入用户名'})
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'),
                                               Length(min=6, max=12, message='密码在6到12位')],
                             render_kw={'placeholder': '请输入密码'})
    password_two = PasswordField('确认密码', validators=[equal_to('password', message='两次密码不一致')],
                                 render_kw={'placeholder': '请输入确认密码'})
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='请输入正确的邮箱')],
                        render_kw={'placeholder': '请输入邮箱'})
    submit = SubmitField('注册')

    # 判断用户名和邮箱是否唯一
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户已存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已存在')


# 登陆表单
class Login(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'),
                                              Length(min=6, max=12, message='用户名在6到12位')],
                           render_kw={'placeholder': '请输入用户名'})
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'),
                                               Length(min=6, max=12, message='密码在6到12位')],
                             render_kw={'placeholder': '请输入密码'})
    submit = SubmitField('登陆')

    # 判断用户名是否存在
    def validate_username(self, field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户不存在')


# 修改头像类
class Icon(FlaskForm):
    icon = FileField('头像', validators=[FileRequired(message='头像不能为空'),
                                       FileAllowed(['jpg', 'jpeg', 'gif', 'png'], message='请上传正确的格式图片')])
    submit = SubmitField('修改')


# 修改用户名类
class Username(FlaskForm):
    username = StringField('当前用户名', validators=[DataRequired(message='用户名不能为空'),
                                                Length(min=6, max=12, message='用户名在6到12位')],
                           render_kw={'placeholder': '请输入用户名'})
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'),
                                               Length(min=6, max=12, message='密码在6到12位')],
                             render_kw={'placeholder': '请输入密码'})
    username_name = StringField('新用户名', validators=[DataRequired(message='用户名不能为空'),
                                                    Length(min=6, max=12, message='用户名在6到12位')],
                                render_kw={'placeholder': '请输入用户名'})
    submit = SubmitField('修改')


# 修改密码类
class ChangePassword(FlaskForm):
    username = StringField('当前用户名', validators=[DataRequired(message='用户名不能为空'),
                                                Length(min=6, max=12, message='用户名在6到12位')],
                           render_kw={'placeholder': '请输入用户名'})
    password_old = PasswordField('密码', validators=[DataRequired(message='密码不能为空'),
                                                   Length(min=6, max=12, message='密码在6到12位')],
                                 render_kw={'placeholder': '请输入密码'})
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'),
                                               Length(min=6, max=12, message='密码在6到12位')],
                             render_kw={'placeholder': '请输入密码'})
    password_two = PasswordField('确认密码', validators=[equal_to('password', message='两次密码不一致')],
                                 render_kw={'placeholder': '请输入确认密码'})
    submit = SubmitField('修改')


# 修改邮箱类
class Change_email(FlaskForm):
    username = StringField('当前用户名', validators=[DataRequired(message='用户名不能为空'),
                                                Length(min=6, max=12, message='用户名在6到12位')],
                           render_kw={'placeholder': '请输入用户名'})
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'),
                                               Length(min=6, max=12, message='密码在6到12位')],
                             render_kw={'placeholder': '请输入密码'})
    email_old = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='请输入正确的邮箱')],
                            render_kw={'placeholder': '请输入邮箱'})
    email_new = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='请输入正确的邮箱')],
                            render_kw={'placeholder': '请输入邮箱'})
    submit = SubmitField('修改')


# 找回密码
class Recover_password(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='请输入正确的邮箱')],
                        render_kw={'placeholder': '请输入邮箱'})
    submit = SubmitField('确认')



class NewPassword(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'),
                                               Length(min=6, max=12, message='密码在6到12位')],
                             render_kw={'placeholder': '请输入密码'})
    password_two = PasswordField('确认密码', validators=[equal_to('password', message='两次密码不一致')],
                                 render_kw={'placeholder': '请输入确认密码'})
    submit = SubmitField('确认')
