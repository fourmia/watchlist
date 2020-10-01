# Copyright (c) StilesYu  All Rights Reserved.
# File Name: %
# Author: Stiles Yu
# mail: yuxiaochen886@gmail.com
# github:https://github.com/Stilesyu
# blog:http://www.stilesyu.com/
# Created Time: 2020-09-30
from flask import Flask
from flask import url_for, escape
app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000)
