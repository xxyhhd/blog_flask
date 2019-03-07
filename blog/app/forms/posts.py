from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, TextAreaField, BooleanField, RadioField
from wtforms.validators import ValidationError, DataRequired, Length, Email, equal_to
from app.models import Posts


# 发表博客类
class SendPosts(FlaskForm):
    title = StringField('标题', validators=[DataRequired(message='标题不能为空'),
                                          Length(min=1, max=50, message='标题不能超过50字')],
                        render_kw={'placeholder': '请输入标题'})
    article = TextAreaField('内容', validators=[DataRequired(message='内容不能为空')],
                            render_kw={'placeholder': '请输入内容'})
    state = RadioField('是否他人可见', choices=[('1', '是'), ('0', '否')], validators=[DataRequired()])
    # state = BooleanField('是否设为他人可见', default='checked', validators=[DataRequired()])
    submit = SubmitField('发表')


# 博客操作类
class ChangePosts(FlaskForm):
    delete = SubmitField('删除')
    change = SubmitField('修改')
    state = RadioField('是否他人可见', choices=[('1', '是'), ('0', '否')], validators=[DataRequired()])
    attention = SubmitField('关注')
