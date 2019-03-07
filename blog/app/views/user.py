from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.forms import Register, Login  # 导入表单注册类,登陆类
from app.forms.user import Icon, Username, ChangePassword, Change_email, Recover_password, NewPassword
from app.models import User  # 导入user模型类
from app.mail import send_mail
from flask import current_app
from flask_login import login_required, current_user, login_user, logout_user
from flask_uploads import UploadSet, configure_uploads, patch_request_class, IMAGES
import os

user = Blueprint('user', __name__)

# 注册的视图函数
'''
注册功能步骤
1. 判断用户名和邮箱是否唯一
2. 将接收到的表单正确数据进行存储（密码加密存储）
3. 生成token字符串（让用户点击账户激活时，我们知道是谁来激活的）
4. 配置发送邮件的代码
5. 发送邮件携带的token
6. 用户点击进行账号激活
'''


# 注册视图函数
@user.route('/register/', methods=['POST', 'GET'])
def register():
    form = Register()
    if form.validate_on_submit():
        # try:
        # password是加密后的密码
        info = User(username=form.username.data, password=form.password.data, email=form.email.data)
        info.save()
        # 获取token字符串
        token = info.generate_token()
        # 发送邮件
        send_mail('邮件激活', info.email, 'activate', username=info.username, token=token,
                  endpoint='user.activate')
        flash('注册成功，请前往邮箱进行账号的激活')
        return redirect(url_for('user.login'))
        # except:
        #     flash('用户注册失败')
    return render_template('user/register.html', form=form)


# 邮件激活的视图函数
@user.route('/activate/<token>/')
def activate(token):
    if User.check_token(token):
        flash('激活成功')
    else:
        flash('激活失败')
    return redirect(url_for('user.login'))


# 登陆的视图函数
"""
接收到用户数据以后
验证密码是否正确
正确则保持用户登陆状态
错误则重新登陆
"""


@user.route('/login/', methods=['POST', 'GET'])
def login():
    form = Login()
    if form.validate_on_submit():
        try:
            u = User.query.filter(User.username == form.username.data).first()
            if not u.check_password(form.password.data):
                flash('密码错误，请输入正确的密码')
            elif not u.confirm:
                flash('您还未激活，不能登陆')
            else:
                login_user(u)  # 维持当前的登录状态
                return redirect(url_for('main.index'))
        except:
            flash('登陆失败，请重新登陆')
    return render_template('user/login.html', form=form)


# 退出方法
@user.route('/logout/')
def logout():
    logout_user()  # 退出登录状态
    flash('退出成功')
    return redirect(url_for('main.index'))


# 设置随机名称的函数
def random_name(suffix, length=64):
    import string, random
    pattern = string.ascii_letters + string.digits
    return ''.join(random.choices(pattern, k=length)) + suffix


# 添加修改头像
@user.route('/change_icon/', methods=['POST', 'GET'])
def change_icon():
    from PIL import Image
    form = Icon()
    new_name = None
    # img_url = current_user
    if not current_user.is_authenticated:
        flash('请先登录再修改')
    # data = User.query.filter(User.username == current_user)
    elif form.validate_on_submit():
        file = request.files.get('icon')
        suffix = os.path.splitext(file.filename)[-1]
        new_name = random_name(suffix)
        UPLOD_FOLDER = os.path.join(os.getcwd(), 'app\\static\\upload')
        path = os.path.join(UPLOD_FOLDER, new_name)
        file.save(path)
        img = Image.open(path)
        img.thumbnail((100, 100))
        img.save(path)
        current_user.icon = new_name
        User.save(current_user)
    return render_template('user/change_icon.html', form=form, filename=new_name)


# 显示个人信息
@user.route('/my_info/')
@login_required
def my_info():
    u = User.query.get(current_user.id)
    return render_template('user/my_info.html', u=u)


# 修改用户个人用户名
@user.route('/change_account/', methods=['POST', 'GET'])
def change_username():
    form = Username()
    if current_user.is_authenticated:
        logout_user()
    if form.validate_on_submit():
        try:
            u = User.query.filter(User.username == form.username.data).first()
            if not u:
                flash('用户名不存在，请输入正确的用户名')
            if not u.check_password(form.password.data):
                flash('密码错误，请输入正确的密码')
            if User.query.filter(User.username == form.username_name.data).first():
                flash('新用户名已存在，请输入其他的用户名')
            else:
                u.username = form.username_name.data
                User.save(u)
                flash('修改成功，请登录')
                return redirect(url_for('user.login'))
        except:
            flash('修改失败，请重新修改')
    return render_template('user/change_username.html', form=form)


# 修改用户密码
@user.route('/change_password/', methods=['POST', 'GET'])
def change_password():
    form = ChangePassword()
    if current_user.is_authenticated:
        logout_user()
    if form.validate_on_submit():
        try:
            u = User.query.filter(User.username == form.username.data).first()
            if not u:
                flash('用户名不存在，请输入正确的用户名')
            if not u.check_password(form.password_old.data):
                flash('旧密码错误，请输入正确的密码')
            else:
                u.password = form.password.data
                User.save(u)
                flash('修改成功，请登录')
                return redirect(url_for('user.login'))
        except:
            flash('修改失败，请重新修改')
    return render_template('user/change_password.html', form=form)


# 修改邮箱
@user.route('/change_email/', methods=['POST', 'GET'])
def change_email():
    form = Change_email()
    if form.validate_on_submit():
        try:
            u = User.query.filter(User.username == form.username.data).first()
            if not u.check_password(form.password.data):
                flash('密码错误，请输入正确的密码')
            if u.email != form.email_old.data:
                flash('之前的邮箱不正确')
            if User.query.filter(User.email == form.email_new.data).first():
                flash('新邮箱已被其他账号绑定，请更改')
            else:
                u.email = form.email_new.data
                u.confirm = False
                u.save()
                # 获取token字符串
                token = u.generate_token()
                # 发送邮件
                send_mail('邮件激活', u.email, 'activate', username=u.username, token=token,
                          endpoint='user.activate')
                flash('修改成功，请前往邮箱进行账号的激活')
                return redirect(url_for('user.login'))
        except:
            flash('修改失败，请重新修改')
    return render_template('user/change_email.html', form=form)


# 邮件激活的视图函数
@user.route('/activate_password/<token>/', methods=['POST', 'GET'])
def activate_password(token):
    form = NewPassword()
    if User.check_token(token):
        from itsdangerous import TimedJSONWebSignatureSerializer as Seralize  # 导入生成token的模块
        s = Seralize(current_app.config['SECRET_KEY'])
        # 在解析和激活操作过程中，有任何异常都会激活失败
        id = s.loads(token)['id']
        if form.validate_on_submit():
            u = User.query.get(int(id))
            u.password = form.password.data
            User.save(u)
            flash('修改成功，请登录')
            return redirect(url_for('user.login'))
        return render_template('user/password_recover.html', form=form)
    else:
        flash('找回密码失败')
    return render_template('user/password_recover.html', form=form)


@user.route('/recover_password/', methods=['POST', 'GET'])
def recover_password():
    form = Recover_password()
    if form.validate_on_submit():
        u = User.query.filter(User.email == form.email.data).first()
        if not u:
            flash('邮箱不正确')
            return redirect(url_for('user.login'))
        else:
            # 获取token字符串
            token = u.generate_token()
            # 发送邮件
            send_mail('邮件激活', u.email, 'activate_password', username=u.username, token=token,
                      endpoint='user.activate_password')
            flash('修改密码邮件已发送，请去邮箱确认')
            return redirect(url_for('user.login'))
    return render_template('user/recover_password.html', form=form)


# @user.route('/password_recover/')
# def password_recover():
#     form = NewPassword()
#     pass
