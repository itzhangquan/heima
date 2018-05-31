# coding:utf8


from  flask import Flask, jsonify
from flask import g
from flask import make_response
from flask import request
from flask import session
from flask import url_for
from flask.ext.script import Manager

app = Flask(__name__)


app.debug =True
# class Config(object):
#     DEBUG = True
#
#
# app.config.ini.from_object(Config)
# app.config.from_pyfile("./config.ini")
manager = Manager(app)
app.config["SECRET_KEY"] = "dsfgbhhdgfdsdfgdfsaxdc"


@app.before_first_request
def before_first_request():
    print "before_first_reques"
    g.user = "tt"


@app.before_request
def before_request():
    print "before_request"


@app.route('/')
def return_data():
    dict = {"name": "zhangquan", "lover": "jianghuan"}
    dd = jsonify(dict)
    response = make_response(dd)
    response.status = "399 OK"
    response.headers["name"] = "jianghuan"

    response.headers["content-type"] = "html"

    return response
    # return response


@app.route('/banzhang/<int:id>')
def banzhang(id):
    return "我没有钱，请找 <a href ='%s'>副班长<a/>" % url_for("fubanzhang", token=id)


@app.route('/fubanzhang<int:token>')
def fubanzhang(token):
    if token == 100:
        return "借你１００块"
    else:
        return "手头正紧"


@app.route('/set_cookie')
def set_cookie():
    response = make_response("woaijianghuan")
    response.set_cookie("name", "zhangsan")
    response.set_cookie("age", "13", 10000)
    return response


@app.route('/get_cookie')
def get_cookie():
    name = request.cookies.get("name")
    age = request.cookies.get("age")

    return "my lover is %s,her old is %s" % (name, age)


@app.route('/set_session/<name>')
def set_session(name):
    session["name"] = name
    session["age"] = "13"
    return "hello"


@app.route('/get_session')
def get_session():
    name = session.get("name")
    age = session.get("age")
    return "my lover is %s,her old is %s" % (name, age)


@app.after_request
def after_request(resp):
    print "after_request"
    print g.user
    return resp


@app.teardown_request
def teardown_request(e):
    print "teardown_request"
    return e


if __name__ == '__main__':
    manager.run()
# coding:utf8
# """
# cookie: 用来记录用户和服务器的交互数据,比如,链接的状态信息,sessionID,csrf_token, 由服务器进行设置
# cookie的设置: reponse.set_cookie(key,value,maxAge): maxAge表示过期时间, 如果不设置默认一次回话结束
# cookie的获取: request.cookies[key]
#
# """""
# from flask import Flask,make_response,request
# app = Flask(__name__)
#
# @app.route('/set_cookie')
# def set_cookie():
#
#     response = make_response("set_cookie")
#     response.set_cookie("name","zhangsan")
#     response.set_cookie("age","13",10) #10秒有效期
#
#     return response
#
#
# @app.route('/get_cookie')
# def get_cookie():
#
#     #如果使用中括号的形式获取,不存在就会报错, 如果使用get,不存在返回none
#     name = request.cookies.get("name")
#     age = request.cookies.get("age")
#
#     return "name is %s, age is %s"%(name,age)
#
# if __name__ == "__main__":
#     app.run(debug=True)
