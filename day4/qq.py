#coding:utf8
"""
状态码说明:
code: 1 表示账号或者密码为空
code: 0 表示账号密码正确
code: 2 表示账号密码错误

"""""

from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

@app.route('/login',methods=['POST'])
def login():

    #1.获取参数,用户名,密码
    username = request.form.get("username")
    password = request.form.get("password")

    #测试调试模式
    # 1 / 0

    #2.校验
    #2.1验证为空的情况
    if not all([username,password]):
        return jsonify(code=1,msg="账号或者密码为空")

    #2.2验证账号密码的正确性
    if username == "admin" and password == "123":
        return jsonify(code=0,msg='账号密码正确')
    else:
        return jsonify(code=2, msg='账号或者密码不正确')


if __name__ == "__main__":
    app.run(debug=True)