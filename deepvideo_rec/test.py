#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/7/26 上午10:38
# @Author : xiaowei
# @Site : 
# @File : test.py
# @Software: PyCharm

from flask import Flask,render_template,url_for

app=Flask(__name__,template_folder="templates",static_url_path="")

app.debug=True

@app.route('/')
def first_flask():
    return render_template("index.html")


@app.route('/html')
def test_html():
    print("success")
    return render_template("index.html")


if __name__ == '__main__':
    app.run()