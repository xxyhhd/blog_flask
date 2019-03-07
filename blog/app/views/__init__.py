from .main import main  # 导入首页的蓝本文件
from .user import user  # 导入登陆注册的蓝本文件
from .posts import posts  # 导入博客的蓝本文件
from .owncenter import own
# 蓝本对象的列表
default_blueprint = [
    (main, ''),
    (user, ''),
    (own, ''),
    (posts, '')
]


def register_blueprint(app):
    for blueprint, prefix in default_blueprint:
        app.register_blueprint(blueprint, url_prefix=prefix)

