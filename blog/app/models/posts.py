from app.extensions import db
from .db_base import DB  # 导入模型操作的基类
from datetime import datetime


class Posts(db.Model, DB):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    article = db.Column(db.Text)
    pid = db.Column(db.Integer, default=0)  # 无限级分类，多级评论用，comment id
    path = db.Column(db.String(255), default='0,')
    visit = db.Column(db.Integer, default=0)  # 访问量
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())  # 时间
    state = db.Column(db.Boolean, default=True)  # 是否设为他人可见
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))  # 添加外键，可以通过博客获取作者，也可以通过作者查询博客

    comment = db.relationship('Comment', backref='post', lazy='dynamic')
