from flask_sqlalchemy import SQLAlchemy  # ORM模型，sql语句
from flask_bootstrap import Bootstrap  # 注册蓝本
from flask_migrate import Migrate  # 数据库迁移
from flask_mail import Mail  # 处理邮件
from flask_login import LoginManager  # 用户登录状态管理模块
from flask_moment import Moment # 处理时间

# 实例化ORM模型
db = SQLAlchemy()
migrate = Migrate(db=db)
mail = Mail()
login_manager = LoginManager()
moment = Moment()


# 加载app
def ext_int(app):
    db.init_app(app)  # 数据库
    Bootstrap(app)
    migrate.init_app(app=app)
    mail.init_app(app)
    moment.init_app(app)

    # 用户登录状态管理
    login_manager.init_app(app)
    # 处理登录的端点，当访问需要登录之后才能访问的路由，先跳到登录页面
    login_manager.login_view = 'user.login'
    login_manager.login_message = '请先登录再访问'
    login_manager.session_protection = 'strong'  # 最强保护级别，出现任何问题都会退出
