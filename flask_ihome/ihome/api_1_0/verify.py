# coding=utf8
import random
import re

from flask import current_app, jsonify
from flask import json
from flask import request

from ihome import constants
from ihome import redis_store
from ihome.api_1_0 import api
from ihome.utils.captcha.captcha import captcha
from ihome.utils.response_code import RET


@api.route("/sms_code", methods=["post"])
def get_sms_code():
    json_data = request.data
    dict_data = json.loads(json_data)
    mobile = dict_data.get("mobile")
    image_code = dict_data.get("image_code")
    image_code_id = dict_data.get("image_code_id")

    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    if not re.match(r"1[34578]\d{9}", mobile):
        return jsonify(errno=RET.DATAERR, errmsg="手机号格式不正确")

    try:
        redis_image_code = redis_store.get("image_code:%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码获取失败")
    try:
        redis_store.delete("imge_code:%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
    if image_code != redis_image_code:
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码填写错误")
    sms_code = "%06d" % random.randint(0, 999999)

    current_app.logger.debug("短信验证码是:%s" % sms_code)

    try:
        redis_store.set("sms_code:%s"%mobile,sms_code,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg= "短信验证码保存失败")
    return jsonify(errno=RET.OK,errmsg="发送成功")


@api.route("/image_code")
def get_image_code():
    cur_id = request.args.get("cur_id")
    pre_id = request.args.get("pre_id")

    name, text, image_data = captcha.generate_captcha()
    try:
        redis_store.set("image_code:%s" % cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
        if pre_id:
            redis_store.delete("image_code" % pre_id)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="验证码保存失败")
