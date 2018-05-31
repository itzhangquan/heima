#coding:utf8
from threading import Thread

from flask import Flask
from flask import url_for

app = Flask(__name__)

from flask_mail import Mail, Message

app.config["MAIL_SERVER"]="smtp.163.com"
app.config["MAIL_USERNAME"]="zhqujahu@163.com"
app.config["MAIL_PASSWORD"]="zyq687294"
app.config["MAIL_PORT"]=465
app.config["MAIL_USE_SSL"]=True
app.config["MAIL_DEFAULT_SENDER"]="zhqujahu@163.com"

mail=Mail(app)
#
@app.route('/')
def index():
    return "<a href='%s'>发送</a>"%url_for("send_mail")

@app.route('/send_mail')
def send_mail():
    message = Message()
    message.subject="静夜思"
    message.recipients=["zhqujahu@163.com"]
    message.html =  "<h1>床前我明月光, 疑似他地上霜,举头那望明月,低头这思故乡</h1>"
    thread =Thread(target=async_send,args=(app,message))
    thread.start()
    return "发送成功"


def async_send(app,message):
    with app.app_context():
        mail.send(message)


if __name__ == '__main__':
    app.run(debug=True)
# #coding:utf8
# """
# flask_mail: 用于发送邮件的扩展包
# 使用流程:
# 1. 进行配置,配置邮箱的账号,授权码,端口,ip..
# 2. 创建邮件客户端,关联app
# 3. 创建消息体
# 4. 使用客户端, 发送消息体
#
# """""
# from threading import Thread
#
# from flask import Flask
# from flask import url_for
# from flask_mail import Mail, Message
#
# app = Flask(__name__)
#
# #设置配置信息
# app.config["MAIL_SERVER"] = "smtp.163.com" #邮件服务器的地址
# app.config["MAIL_USERNAME"] = "zhqujahu@163.com" #邮件用户名
# app.config["MAIL_PASSWORD"] = "zyq687294" #授权码
# app.config["MAIL_PORT"] = 465 # 网易邮箱固定发送端口
# app.config["MAIL_USE_SSL"] = True #安全加密套接字传输
# app.config["MAIL_DEFAULT_SENDER"] = "zhqujahu@163.com" #默认的邮件发送者
#
#
# #创建邮件客户端
# mail = Mail(app)

# @app.route('/')
# def index():
#
#
#     return "<a href='%s'>发送</a>"%url_for("send_mail")
#
# @app.route('/send_mail')
# def send_mail():
#     #创建消息体
#     message = Message()
#     message.subject = "静夜思"
#     message.recipients = ["zhqujahu@163.com" ]
#     # message.body = "床前我明月光, 疑似他地上霜,举头那望明月,低头这思故乡"
#     message.html = "<h1>床前我明月光, 疑似他地上霜,举头那望明月,低头这思故乡</h1>"
#
#     # import time
#     # time.sleep(10)
#
#     #发送邮件
#     # mail.send(message)
#
#     #通过子线程的方式发送
#     thread = Thread(target=async_send,args=(app,message))
#     thread.start()
#
#     return "发送成功"

# def async_send(app,message):
#     #开启子线程中的上线文
#     with app.app_context():
#         mail.send(message)
#         import time
#         time.sleep(10)
#
#
# if __name__ == "__main__":
#     app.run(debug=True)

