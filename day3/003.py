# coding:utf8
from flask import Flask
from flask import render_template
from flask.ext.wtf import FlaskForm, form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.config["SECRET_KEY"] = "dfghnjgfdfvcsa"


class Myform(FlaskForm):
    username = StringField(u"用户名", validators=[DataRequired()])
    password = PasswordField(u"密码", validators=[DataRequired()])
    repassword = PasswordField(u"密码", validators=[DataRequired(), EqualTo("password")])
    submit =SubmitField(u"提交")
#

# @app.route('/')
# def index():
#
#     form = Myform()
#
#     return render_template("03.html",form=form)
@app.route('/')
def index():
    form = Myform()
    
    return render_template("03.html",form=form)
# @app.route('/register',methods=["POST"])
# def register():
#     if form.validate_on_submit():
#         username=form.username.data
#         password=form.password.data
#         repassword=form.repassword.data
#
#
#         print username
#         print password
#         print repassword
#
#         return "注册成功"
#     return "注册失败"
# if __name__ == '__main__':
#     app.run(debug=True)

#coding:utf8
# """
# flask_WTF表单: 通过字段的方式显示界面,通过函数验证表单中的值
#  好处: 维护更加方便, 提供csrf验证
#
# 使用流程:
# 1. 属于flask中的扩展包,需要安装
# 2. 定义类,继承自FlaskForm
# 3. 在类中编写字段,编写函数验证字段
# 4. 创建表单类,渲染到页面中
#
# 注意点:
# 1. wtform表单提供了csrf验证机制
# 2. csrf_token的生成依赖SECRET_KEY
# 3. 通过validate_on_submit验证字段中的验证信息,会对'POST', 'PUT', 'PATCH', 'DELETE'提交方式校验
# 4. 获取表单中内容的方法: form.字段.data
# """""
#
# from flask import Flask
# from flask import render_template
# from flask.ext.wtf import FlaskForm
# from wtforms import StringField,PasswordField,SubmitField
# from wtforms.validators import  DataRequired,EqualTo
#
# app = Flask(__name__)
# app.config["SECRET_KEY"] = "djfkdkfjd"
#
# # 2. 定义类,继承自FlaskForm
# class Myform(FlaskForm):
#     username = StringField(u'用户名',validators=[DataRequired()])
#     password = PasswordField(u'密码',validators=[DataRequired()])
#     repassword = PasswordField(u'确认密码',validators=[DataRequired(),EqualTo('password')])
#     submit = SubmitField(u'提交')


# @app.route('/')
# def index():
#
#     form = Myform()
#
#     return render_template("03.html",form=form)

@app.route('/register', methods=['POST'])
def register():

    #1.获取参数
    form = Myform()

    #2.校验参数, validate_on_submit验证字段中的验证信息
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        repassword = form.repassword.data

        print username
        print password
        print repassword

        return "注册成功"

    #3.返回注册信息
    return "注册失败"




if __name__ == "__main__":
    app.run(debug=True)