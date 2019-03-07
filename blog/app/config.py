import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 密钥
    SECRET_KEY = '123QWE'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 发送邮件的配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'xxxxxxxxx@qq.com'  # 邮箱
    MAIL_PASSWORD = 'xxxxxxxxx'  # 邮箱授权码
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # 在环境中获取密码
    # 每页显示数据的条数，分页使用
    PAGE_NUM = 3

    # UPLOADED_PHOTOS_DEST = os.path.join(os.path.dirname(os.getcwd()), 'static/upload')
    # MAX_CONTENT_LENGTH = 1024*1024*64


# 开发环境的配置
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456789@127.0.0.1:3306/flask_blog'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'data-dev.sqlite')


# 测试环境的配置
class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456789@127.0.0.1:3306/flask_blog_test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-test.sqlite')


# 生成环境的配置
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456789@127.0.0.1:3306/flask_blog_real'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog.sqlite')


# 配置类的别名
config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
