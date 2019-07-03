from flask import Blueprint, render_template, request, redirect, url_for, session
from App.models import *

blue = Blueprint('blog', __name__)

#      --------------------------------前端--------------------------------------
# 首页
@blue.route('/')
def index():
    # 文章列表
    columns = MyColumn.query.all()

    articles = Article.query.all()

    return render_template('home/index.html',columns=columns,articles=articles)


# 文章栏目分类
@blue.route('/column/<int:id>/')
def article_column(id):
    columns = MyColumn.query.all()

    #被搜索的栏目
    column = MyColumn.query.get(id)
    articles = column.articles
    print(column.articles)

    return render_template('home/column.html', columns=columns, articles=articles)


# 文章详情与评论
@blue.route('/articledatail/<int:id>/')
def article_datail(id):
    columns = MyColumn.query.all()
    article = Article.query.get(id)
    return render_template('home/article_detail.html',columns=columns,article=article)






#      --------------------------------后台--------------------------------------
# 后台登录
@blue.route('/admin/login/',methods=['GET','POST'])
def admin_login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('userpwd')

        # 进行验证配对
        user = SuperUser.query.filter_by(name=username,password=password).first()
        # 登录成功
        if user:
            # 设置session
            session['username'] = username
            return redirect(url_for('blog.admin_index'))
        # 登录失败
        else:
            return render_template('admin/login.html',msg='用户名或密码错误')

    return render_template('admin/login.html')


# 后台注册
@blue.route('/admin/register/',methods=['GET','POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('userpwd1')
        password2 = request.form.get('userpwd2')

        # 进行验证配对
        user = SuperUser.query.filter_by(name=username).first()
        # 若存在
        if user:
            return render_template('admin/register.html', msg='用户名已存在')
            # 若不存在则创建
        else:
            if password != password2:
                return render_template('admin/register.html', msg='密码不一致')

            user = SuperUser()
            user.name = username
            user.password = password

            try:
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('blog.admin_login'))
                # return render_template('admin/register.html',msg='添加栏目成功')
            except:
                db.session.rollback()
                db.session.flush()
                return render_template('admin/register.html', msg='注册用户失败')

    return render_template('admin/register.html')

# 后台主页
@blue.route('/admin/')
def admin_index():
    username = session.get('username','')
    if username:
        return render_template('admin/index.html',username=username)
    else:
        return redirect(url_for('blog.admin_login'))


# 后台栏目
@blue.route('/admin/column/',methods=['GET','POST'])
def admin_column():
    # 获取所有的栏目
    columns = MyColumn.query.filter_by()

    if request.method == 'GET':
        return render_template('admin/category.html',columns=columns)
    elif request.method == 'POST':
        # 增加栏目，并添加的属性
        acolumn = MyColumn()
        acolumn.name = request.form.get('name')
        acolumn.other_name = request.form.get('alias')
        acolumn.key_word = request.form.get('keywords')
        acolumn.desc = request.form.get('describe')

        try:
            db.session.add(acolumn)
            db.session.commit()
            return render_template('admin/category.html',columns=columns,msg='添加栏目成功')
        except:
            db.session.rollback()
            db.session.flush()
            return render_template('admin/category.html',columns=columns, msg='添加栏目失败')


# 栏目修改
@blue.route('/admin/updatecolumn/<int:id>/',methods=['GET','POST'])
def admin_update_column(id):
    if request.method == 'GET':
        acolumn = MyColumn.query.get(id)
        return render_template('admin/update-category.html',acolumn=acolumn)

    elif request.method == 'POST':
        acolumn = MyColumn.query.get(id)
        acolumn.name = request.form.get('name')
        acolumn.other_name = request.form.get('alias')
        acolumn.key_word = request.form.get('keywords')
        acolumn.desc = request.form.get('describe')

        try:
            db.session.add(acolumn)
            db.session.commit()
            return redirect(url_for('blog.admin_column'))
        except:
            db.session.rollback()
            db.session.flush()
            return render_template('admin/update-category.html', acolumn=acolumn ,msg='修改栏目失败')


# 栏目删除
@blue.route('/admin/delcolumn/<int:id>/')
def admin_del_column(id):
    acolumn = MyColumn.query.get(id)

    try:
        db.session.delete(acolumn)
        db.session.commit()
        return redirect(url_for('blog.admin_column'))
    except:
        db.session.rollback()
        db.session.flush()
        return 'fail'



# 后台文章
@blue.route('/admin/article/')
def admin_article():
    articles = Article.query.all()
    return render_template('admin/article.html',articles=articles)


# 增加文章
@blue.route('/admin/addarticle/',methods=['GET','POST'])
def admin_add_article():
    columns = MyColumn.query.all()

    if request.method == 'GET':
        return render_template('admin/add-article.html',columns=columns)
    elif request.method == 'POST':
        article = Article()
        article.title = request.form.get('title')
        article.key_word = request.form.get('keywords')
        article.content = request.form.get('content')
        article.desc = request.form.get('describe')
        article.tag = request.form.get('tags')
        article.my_column = request.form.get('category')

        try:
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('blog.admin_article'))
        except:
            db.session.rollback()
            db.session.flush()
            return render_template('admin/add-article.html',columns=columns,msg='添加栏目失败')


# 修改文章
@blue.route('/admin/updatearticle/<int:id>/',methods=['GET','POST'])
def admin_upgrade_article(id):
    columns = MyColumn.query.all()

    if request.method == 'GET':
        article = Article.query.get(id)
        return render_template('admin/update-article.html',article=article,columns=columns)

    elif request.method == 'POST':
        article = Article.query.get(id)
        article.title = request.form.get('title')
        article.content = request.form.get('content')
        article.key_word = request.form.get('keywords')
        article.desc = request.form.get('describe')
        article.tag = request.form.get('tags')
        article.my_column = request.form.get('category')

        try:
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('blog.admin_article'))
        except:
            db.session.rollback()
            db.session.flush()
            return render_template('admin/update-article.html', article=article, columns=columns,msg='修改文章失败')



# 文章删除
@blue.route('/admin/delarticle/<int:id>/')
def admin_del_article(id):
    article = Article.query.get(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect(url_for('blog.admin_article'))
    except:
        db.session.rollback()
        db.session.flush()
        return 'fail'







