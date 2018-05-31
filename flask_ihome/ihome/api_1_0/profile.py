#coding:utf8
from flask import current_app
from flask import g
from flask import request
from flask import session, jsonify

from ihome import constants
from ihome import db
from ihome.api_1_0 import api
from ihome.models import User
from ihome.utils.commons import login_required
from ihome.utils.image_storage import image_storage
from ihome.utils.response_code import RET


@api.route("/user")
def get_user_info():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify(errno=RET.NODATA, errmsg="用户未曾登录")
    try:
        user = User.query.get(user_id)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库查询异常")
    if not user:
        return jsonify(errno=RET.NODATA, errmsg="该用户不存在")

    user_dict = {
        "user_id": user.id,
        "name": user.name,
        "mobile": user.mobile,
        "avatar_url": "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1526278082526&di=df87f3eb13ef16854a1c59524ea44fd2&imgtype=0&src=http%3A%2F%2Fwww.ld12.com%2Fupimg358%2Fallimg%2F20160629%2F120625879334259.jpg"
    }
    return jsonify(errno=RET.OK, errmsg="获取成功", data=user_dict)




@api.route("/user/avater", method=["POST"])
@login_required
def upload_image():
    avater = request.files.get("avater")
    image_data = avater.read
    user_id = g.user_id

    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="查询失败")
    if not user:
        return  jsonify(errno=RET.NODATA,errmsg="该用户不存在")

    try:
        image_name = image_storage(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR,errmsg="上传失败")

    if image_name:
        user.avatar_url=image_name

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="头像更新失败")

    avatar_url = constants.QINIU_DOMIN_PREFIX+image_name
    return  jsonify(errno=RET.DBERR,errmsg="上传成功",date={"avatar_url":avatar_url})

@api.route("/user/name",method=["PUT"])
@login_required
def update_user_name():
    name = request.json.get("name")
    user_id = g.user.id

    try:
        user=User.query.filter(User.id==user_id).first()
    except:
        return jsonify(errno=RET.DBERR,errmsg="查询失败")

    if not user:
        return jsonify(errno=RET.NODATA,errmsg="该用户不存在")

    user.name=name

    try:
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库更新异常")

        # 6.返回修改状态
    return jsonify(errno=RET.OK, errmsg="更新用户名成功")


@api.route("/user/auth",method=["POST"])
@login_required

def set_user_auth():
    real_name=request.json.get('real_name')
    id_card = request.json.get("id_card")

    if not all ([real_name,id_card]):
        return  jsonify(errno=RET.PARAMERR,errmsg="参数不完整")
    user_id = g.user_id
    try:
        user= User.query.filter(User.id==user_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="数据库查询异常")

    if not user:
        return jsonify(errno=RET.NODATA,errmsg="没有该用户")
    user.id_card = id_card
    user.real_name =real_name

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据更新失败")

        # 7.返回前端页面
    return jsonify(errno=RET.OK, errmsg="更新成功")







