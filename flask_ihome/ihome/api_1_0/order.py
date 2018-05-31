#coding:utf8
from datetime import datetime

from flask import current_app
from flask import g
from flask import request, jsonify

from ihome import db
from ihome.api_1_0 import api
from ihome.models import House, Order
from ihome.utils.commons import login_required
from ihome.utils.response_code import RET


@api.route("/orders",method =["POST"])
@login_required
def create_order():
    house_id = request.get_json().get("housed_id")
    start_date_str= request.get_json().get("start_date")
    end_date_str = request.get_json().get("end_date")

    if not all([house_id,start_date_str,end_date_str]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不完整")
    try:
        house = House.query.get(house_id)
        start_date=datetime.striptime(start_date_str,"%Y-%m-%d")
        end_date = datetime.strptime(end_date_str,"%Y-%m-%d")

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errrno = RET.DBERR,errmsg= "查询异常")

    if not house:
        return  jsonify(errno=RET.NODATA,errmsg="＝该房子不存在")

    try:
        conflict_orders= Order.query.filter(start_date<Order.end_date,end_date>Order.start_date)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg= "查询订单异常")
    if conflict_orders:
        return  jsonify(errno=RET.DATAERR,errmsg ="该房子时间段内已被锁定")
    order= Order()
    days =(end_date-start_date).days
    order.user_id = g.user_id
    order.user_id = g.user_id
    order.house_id = house_id
    order.begin_date = start_date
    order.days = days
    order.house_price = house.price
    order.amount = house.price*days


    try:
        db.session.add(order)
        db.session.commit()

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="订单创建失败")

    return jsonify(errno=RET.OK,errmsg="创建成功")

@api.route("/orders/<int:order_id",method=["put"])
def receive_reject_order(order_id):
    action = request.args.get("action")
    if not order_id or not action in ["accept","reject"]:
        return jsonify(errno=RET.PARAMERR,errmsg= "参数不完整")

    try:
        order= Order.query.get(order_id)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询异常")

    if action =="accept":
        order.status="REJECTED"
        order.comment = request.json.get("reason","")

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="更新失败")

    return jsonify(errno=RET.OK,errmsg="更新成功")


@api.route("/orders/<int:order_id>/comment",method=["PUT"])
@login_required
def send_comment(order_id):
    comment=request.json.get("comment")
    if not all ([order_id,comment]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不完整")


    try:
        order = Order.query.get(order_id)
        assert order.user_id == g.user_id,"不是同一人"

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="获取订单异常")


    if not order:
        return jsonify(errno=RET.NODATA,errmsg="该定单不存在")

    order.status="COMPILE"
    order.comment = comment

    try:
        db.session.commit()

    except Exception as e:
        current_app.logger.error(e)
        return  jsonify(errno=RET.DBERR,errmsg="更新失败")
    i
    return jsonfy(errno=RET.OK,errmsg="发表更新成功")



