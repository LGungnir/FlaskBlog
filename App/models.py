from datetime import datetime

from App.exts import db


# 管理员
class SuperUser(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))


#栏目：文章 = 1：n
# 栏目
class MyColumn(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(32), unique=True)                #名称
    other_name = db.Column(db.String(32))                       #别名
    key_word = db.Column(db.String(32))                         #关键字
    desc = db.Column(db.String(255))                            #描述

    # 文章反查
    articles = db.relationship('Article',backref='column',lazy=True)


# 文章
class Article(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(32), unique=True)                                   # 标题
    content = db.Column(db.String(2048))                                            # 内容
    key_word = db.Column(db.String(32))                                             # 关键字
    desc = db.Column(db.String(255))                                                # 描述
    tag = db.Column(db.String(32),default='Python')                                 # 标签
    atime = db.Column(db.DateTime, default=datetime.now().strftime("%Y-%m-%d %X"))  # 时间

    # 栏目外键
    my_column = db.Column(db.Integer,db.ForeignKey(MyColumn.id))



