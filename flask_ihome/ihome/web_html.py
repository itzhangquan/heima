#coding:utf8
from flask import Blueprint
from flask import current_app
from flask.ext.wtf.csrf import generate_csrf

web_html = Blueprint('web_html', __name__)

@web_html.route('/<re(r".*"):file_name>')
def get_static_html(file_name):
    # 判断file_name是否有内容
    if not file_name:
        file_name = "index.html"

    # 判断如果不是favicon.ico的情况下才做拼接
    if file_name != "favicon.ico":
        file_name = "html/" + file_name

    # 调用send_static_file方法，获取static文件底下的资源，返回response对象
    response = current_app.send_static_file(file_name)


    csrf_token = generate_csrf()
    response.set_cookie("csrf_token",csrf_token)
    return response

