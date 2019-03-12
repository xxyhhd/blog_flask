from app.extensions import db
from .db_base import DB  # 导入模型操作的基类
from flask import current_app  # 使用当前的app
from werkzeug.security import generate_password_hash, check_password_hash  # 导入hash加密模块
from itsdangerous import TimedJSONWebSignatureSerializer as Seralize  # 导入生成token的模块
from app.extensions import login_manager
from flask_login import UserMixin
from datetime import datetime
from .posts import Posts

class User(UserMixin, db.Model, DB):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), index=True)
    password_hash = db.Column(db.String(120))
    email = db.Column(db.String(50), index=True)
    age = db.Column(db.Integer, default=18)
    sex = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())  # 时间
    attention = db.Column(db.Text, default='0')
    icon = db.Column(db.String(70), default='default.jpg')
    confirm = db.Column(db.Boolean, default=False)  # 账号是否激活，默认未激活
    """
    posts 是当前user模型的关联属性，可以通过当前用户获取该用户发表的博客
    参数：
        Posts: 建立关联的模型
        backref: 给关联的模型添加字段属性 user
        lazy： 加载时机， 返回查询集，可以再次进行二次过滤：User.query+过滤器，如果
                不加lazy属性，则返回结果的列表
    """
    posts = db.relationship('Posts', backref='user', lazy='dynamic')
    comment = db.relationship(
        'Comment', backref='comment_user', lazy='dynamic')
    # secondary 是多对多时指定数据的中间表
    # backref给另一方的多设置查询结果为查询集，可以进行查询结果的过滤
    favorites = db.relationship('Posts', secondary='collections', backref=db.backref(
        'users', lazy='dynamic'), lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('该属性不可读')

    # 生成加密密码
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码正确性
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成token的方法
    def generate_token(self):
        # 默认token有效期是一小时，可以在Seralize原代码修改
        token = Seralize(current_app.config['SECRET_KEY'])
        # token中携带ID字段
        return token.dumps({'id': self.id})

    # 验证token并进行账号的激活
    @staticmethod
    def check_token(token):
        s = Seralize(current_app.config['SECRET_KEY'])
        # 在解析和激活操作过程中，有任何异常都会激活失败
        try:
            id = s.loads(token)['id']
            u = User.query.get(int(id))
            if not u.confirm:
                u.confirm = True
                u.save()
            return True
        except:
            return False

    # 判断是否收藏的方法
    def is_favorite(self, id):
            favorites = self.favorites.all()
            for f in favorites:
                if f.id == id:
                    return True
            return False

    # 执行收藏的方法
    def add_favorite(self, id):
        self.favorites.append(Posts.query.get(id))
        db.session.commit()


    # 取消收藏的方法
    def del_favorite(self, id):
        self.favorites.remove(Posts.query.get(id))
        db.session.commit()



# 回调函数，实时获取user表中的数据
@login_manager.user_loader  # 这个装饰器会自动查找最新的User对象
def user_loader(userid):
    return User.query.get(int(userid))
