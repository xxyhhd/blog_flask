from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, jsonify
from app.forms import SendPosts  # 导入博客表单
from app.forms import SendComment
from app.forms.posts import ChangePosts
from flask_login import login_required, current_user
from app.models import Posts, User, Comment  # 导入博客模型类
from flask_login import current_user
from sqlalchemy import or_  # 导入或操作

posts = Blueprint('posts', __name__)


# 必须登录后才能发表博客，调用该方法
@posts.route('/send_posts/', methods=['POST', 'GET'])
def send_posts():
    form = SendPosts()
    if not current_user.is_authenticated:
        flash('请先登录再发表')
    elif form.validate_on_submit():
        # print(form.state.data)
        if form.state.data == '0':
            p = False
        else:
            p = True
        info = Posts(title=form.title.data,
                     article=form.article.data, user=current_user, state=p)
        # print(info.get_id())
        info.save()
        if not form.state.data:
            pass

        flash('发表成功')
        return redirect(url_for('posts.send_posts'))
    return render_template('posts/send_posts.html', form=form)


# 显示博客详情的方法
@posts.route('/posts_detail/<int:id>/', methods=['POST', 'GET'])
@login_required
def posts_detail(id):
    p = Posts.query.get(id)
    # a = False
    # if current_user.is_authenticated and (str(id) in current_user.attention.split(',')):
    #     a = True
    # 写评论
    form = SendComment()
    if form.validate_on_submit():
        info = Comment(article=form.article.data,
                       user_id=current_user.id, post_id=id)
        info.save()
        flash('评论成功')
    data = Comment.query.filter(Comment.post_id == id, Comment.comment_user == current_user).order_by(
        Comment.timestamp.desc()).limit(2)
    data_all = Comment.query.filter(Comment.post_id == id).order_by(
        Comment.timestamp.desc()).limit(100)
    return render_template('posts/page_detail.html', p=p, form=form, data=data, data_all=data_all)


# 博客收藏与取消收藏
@posts.route('/dofavorite/')
def dofavorite():
    try:
        # 将id转为int类型
        id = int(request.args.get('id'))
        # 判断是否收藏
        if current_user.is_favorite(id):
            current_user.del_favorite(id)
            return jsonify({'code': 100})
        else:
            current_user.add_favorite(id)
            return jsonify({'code': 200})
    except:
        return jsonify({'code': 500})


# 博客搜索
@posts.route('/search/', methods=['POST', 'GET'])
def search():
    search_info = request.form.get('search', '')
    if not search_info:
        # 接收分页时传递过来的search
        search_info = request.args.get('search', '')
    try:
        page = int(request.arges.get('search', 1))
    except:
        page = 1
    # 搜索范围是标题和内容，并且在展示的时候匹配的内容红色显示
    pagination = Posts.query.filter(or_(Posts.title.contains(search_info), Posts.article.contains(search_info)),
                                    Posts.pid == 0, Posts.state == True).order_by(Posts.timestamp.desc()).paginate(
        page, current_app.config['PAGE_NUM'], False)
    data = pagination.items
    return render_template('posts/search_detail.html', data=data, search_info=search_info, pagination=pagination)
