# Copyright (c) StilesYu  All Rights Reserved.
# File Name: %
# Author: Stiles Yu
# mail: yuxiaochen886@gmail.com
# github:https://github.com/Stilesyu
# blog:http://www.stilesyu.com/
# Created Time: 2020-09-30
import os
import sys
import click

from flask import Flask, render_template
from flask import url_for, escape
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:  # 若为windows系统，使用三个斜线
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #关闭对模型修改的监控
db = SQLAlchemy(app)

@app.cli.command()
def forge():
    db.create_all()
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},              
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year':'1996'},
        {'title': 'King of Comedy', 'year':'1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year':'2008'},
        {'title': 'The Pork of Music','year': '2012'},
        ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')

class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20)) # 名字

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))   # 电影年份



@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)


@app.route('/test')
def test_url_for():
    # 下面是一些调用示例
    print(url_for('hello'))
    print(url_for('user_page', name='yaoyao'))
    print(url_for('user_page', name='dongdong'))
    print(url_for('test_url_for'))
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL
    # 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000)
