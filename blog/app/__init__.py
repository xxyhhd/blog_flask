from flask import Flask
# 导入当前网站的配置类
from app.config import config
# 加载所有的第三方扩展库
from app.extensions import ext_int
# 导入注册的蓝本函数
from app.views import register_blueprint


# 项目初始化方法
def create_app(ConfigName):
    app = Flask(__name__)
    # 加载网站配置，config.py文件
    app.config.from_object(config[ConfigName])
    # 加载所有第三方扩展库
    ext_int(app)
    # 注册蓝本
    register_blueprint(app)
    # 初始化加载自定义过滤器
    add_filter(app)

    return app


# 定义一个加载自定义过滤器的方法
def add_filter(app):
    # 博客内容超过规定字数，显示...
    @app.template_filter()
    def showEllipsis(str, length=5):
        if len(str) > length:
            str = str[0:300] + '...'
        return str

    # 搜索出来的内容替换为红色
    @app.template_filter()
    def replace_red(str, search_info):
        if str:
            str = str.replace(search_info, '<span style=color:red;>'+search_info+'</span>')
        return str
