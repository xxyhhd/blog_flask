from flask_mail import Message
from .extensions import mail
from flask import current_app, render_template
from threading import Thread


# 异步发送邮件
def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, to, temName, **kwargs):
    """
    发送邮件
    :param subject: 主题
    :param to: 接收者
    :param temName: 模板名称
    :return:
    """
    # 获取真实实例化的flask对象app
    app = current_app._get_current_object()
    # 创建邮件对象
    msg = Message(subject=subject, recipients=[to], sender=current_app.config['MAIL_USERNAME'])
    # 浏览器接收显示内容
    msg.html = render_template('email/' + temName + '.html', **kwargs)
    # 创建线程，在新的线程中发送邮件
    thr = Thread(target=async_send_mail, args=(app, msg))
    thr.start()  # 开启线程
