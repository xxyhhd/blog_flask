from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, TextAreaField, RadioField
from wtforms.validators import  DataRequired
from app.models import Comment


# 发表博客类
class SendComment(FlaskForm):
    article = TextAreaField('评论', validators=[DataRequired(message='评论不能为空')],
                            render_kw={'placeholder': '请输入评论'})
    submit = SubmitField('评论')