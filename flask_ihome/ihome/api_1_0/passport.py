# coding:utf8
import re

from flask import current_app
from flask import request, jsonify
from flask import session

from ihome import redis_store, db
from ihome.api_1_0 import api
from ihome.models import User
from ihome.utils.response_code import RET


@api.route("/session", methods=["POST"])
def login():
    dict_data = request.get_json()
    mobile = dict_data.get("mobile")
    password = dict_data.get("mobile")
    password = dict_data.get("password")

    if not all([mobile, password]):
        return jsonify(reeno=RET.PARAMERR, errmsg="参数不完整")

    if not re.match(r"1[3456789]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    if not re.match(r"1[3456789]\d{9}", mobile):
        return jsonify(errno=RET.DATAERR, errmsg="手机号格式错误")

    try:
        login_num =redis_store.get("login_num%s"%mobile)
    except Exception as e:
        current_app.logger.error(e)

        login_num=0
    if not  login_num:
        login_num=0

    try:
        login_num =int(login_num)
    except Exception as e:
        current_app.logger.error(e)

    if login_num>=5:
        return jsonify(errno=RET.DATAERR,errrmsg="今天的次数用完了，明天再来")
    try:
        user=User.query.filter(User.mobile==mobile).first()
    except Exception as e:
        return jsonify(errno=RET.DBERR,errmsg="数据库查询异常")

    if not  user:
        return jsonify(errno=RET.NODATA,errmsg="该用户不存在")

    if not user.check_password(password):
        try:
            redis_store.incr("login_num:%s"%mobile)
            redis_store.expire("login_num:%s"%mobile,20)
        except Exception as e:
            current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg="密码不正确")
    session["user_id"]=user.id
    session["name"]=user.name
    return jsonify(errno=RET.OK,errmsg="登录成功")




@api.route("/user")
def register():
    dict_data = request.json
    mobile = dict_data.get("mobile")
    sms_code = dict_data.get("sms_code")
    password = dict_data.get("password")

    if not all([mobile, sms_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    if not re.match(r"1[3456789]\d{9}", mobile):
        return jsonify(errno=RET.DATAERR, errmsg="手机号码格式不对")
    try:
        redis_sms_code = redis_store.get("sms_code:%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取短信验证码")

    if not redis_sms_code:
        return jsonify(errno=RET.DBERR, errmsg="短信验证码已经过期")

    try:
        redis_store.delete("sms_code:%s" % mobile)
    except Exception as e:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码填写出错")
    user = User()

    user.name = mobile
    user.mobile = mobile
    user.pasword = password

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="用户注册失败")

    return jsonify(errno=RET.OK, errmsg="注册成功")

@api.route("/session")
def get_user_login_state():
    user_id = session.get("user_id")
    if not  user_id:
        return  jsonify(errno=RET.DATAERR,errmsg="该用户没有登录")

    try:
        user=User.query.get(User_id=user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="数据库查询异常")

    user_dict = {
        "user_id":user_id,
        "name":user.name

    }
    return jsonify(errno=RET.OK,errmsg="获取成功",data=user_dict)


@api.route("/session",methods=["DELETE"])
def logout():
    session.pop("user_id")
    session.pop("name")
    return jsonify(errno=RET.OK,errmsg="退出成功")
