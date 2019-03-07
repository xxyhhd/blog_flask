from app.extensions import db
from .db_base import DB  # 导入模型操作的基类
from datetime import datetime


class Comment(db.Model, DB):
    id = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())  # 时间
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 添加外键，可以通过博客获取作者，也可以通过作者查询博客
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))  # 添加外键，可以通过评论获取博客，也可以通过博客查询评论


