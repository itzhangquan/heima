#coding:utf8
from flask import Flask
from flask import render_template
from flask import request

app=Flask(__name__)

@app.route('/')
def index():
    return render_template("02.html")

@app.route('/register',methods=["POST"])
def register():
    form_data = request.form
    username = form_data.get("username")
    password = form_data.get("password")
    repassword = form_data.get("repassword")
    if not all([username,password,repassword]):
        return u"您填写的数据不够完整"
    if password!=repassword:
        return u"您两次输入的密码不一样"
    return "注册成功"

if __name__ == '__main__':
    app.run(debug=True)
