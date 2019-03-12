from flask import render_template, Blueprint, request, current_app, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Posts, Comment
from app.forms import SendPosts, SendComment
from datetime import datetime

own = Blueprint('owncenter', __name__)


@own.route('/posts_manager/')
@login_required  # 这个装饰器作用是必须登录状态才能执行方法
def posts_manager():
    try:
        page = int(request.args.get('page', 1))
    except:
        page = 1
    # 查出自己的博客并按时间降序进行展示
    pagination = Posts.query.filter(Posts.uid == current_user.get_id()).order_by \
        (Posts.timestamp.desc()).paginate(page, current_app.config['PAGE_NUM'], False)
    # 获取当前页面所有数据
    data = pagination.items
    current_username = current_user.username
    return render_template('owncenter/posts_manager.html', data=data, pagination=pagination,
                           current_username=current_username)


# 博客管理 删除
@own.route('/posts_delete/<int:id>/')
@login_required
def posts_delete(id):
    Posts.query.get(id).delete()
    flash('博客删除成功！')
    return redirect(url_for('owncenter.posts_manager'))


# 收藏博客
@own.route('/posts_attention/<int:id>/')
@login_required
def posts_attention(id):
    # attention_list = current_user.attention.split(',')
    # if str(id) not in attention_list:
    #     attention_list.append(str(id))
    #     a = True
    # else:
    #     attention_list.remove(str(id))
    #     a = False
    # print(attention_list)
    # current_user.attention = ','.join([str(i) for i in attention_list])
    # current_user.save()
    # p = Posts.query.get(id)
    # 写评论
    form = SendComment()
    if form.validate_on_submit():
        info = Comment(article=form.article.data, user_id=current_user.id, post_id=id)
        info.save()
        flash('评论成功')
    data = Comment.query.filter(Comment.post_id == id, Comment.comment_user == current_user).order_by \
        (Comment.timestamp.desc()).limit(2)
    data_all = Comment.query.filter(Comment.post_id == id).order_by \
        (Comment.timestamp.desc()).limit(100)
    return render_template('posts/page_detail.html', p=p, data_all=data_all, data=data, form=form)


# 我的收藏
@own.route('/my_attention/', methods=['POST', 'GET'])
@login_required
def my_attention():
    try:
        page = int(request.args.get('page', 1))
    except:
        page = 1
    # 查出我收藏的博客并按收藏时间进行展示
    # attention_list = current_user.attention.split(',')
    # pagination = Posts.query.filter(Posts.id.in_([int(i) for i in attention_list[1:len(attention_list)]])).order_by \
    #     (Posts.timestamp.desc()).paginate(page, current_app.config['PAGE_NUM'], False)
    
    pagination = current_user.favorites.all().paginate(page, current_app.config['PAGE_NUM'], False)
    # 获取当前页面所有数据
    data = pagination.items
    print(pagination)
    print(data)
    # return render_template('main/index.html', p=data, pagination=pagination)
    return render_template('owncenter/my_attention.html', p=data, pagination=pagination)


# 博客修改
@own.route('/edit_posts/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_posts(id):
    form = SendPosts()
    p = Posts.query.get(id)  # 通过博客id查询出博客对象
    if form.validate_on_submit():
        p.title = form.title.data
        p.article = form.article.data
        p.timestamp = datetime.utcnow()
        if form.state.data == '0':
            p.state = False
        else:
            p.state = True
        p.save()
        flash('博客修改成功！')
        # 重定向到博客管理
        return redirect(url_for('owncenter.posts_manager'))
    # 添加默认值
    form.title.data = p.title
    form.article.data = p.article
    return render_template('owncenter/edit_posts.html', form=form)


# 搜索我的博客
@own.route('/search_my_posts/', methods=['POST', 'GET'])
def search_my_posts():
    from sqlalchemy import or_  # 导入或操作
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
                                    Posts.uid == current_user.id).order_by \
        (Posts.timestamp.desc()).paginate(page, current_app.config['PAGE_NUM'], False)
    data = pagination.items
    return render_template('posts/search_detail.html', data=data, search_info=search_info, pagination=pagination)
