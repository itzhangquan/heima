# coding=utf-8
from flask import current_app, jsonify
from flask import g
from flask import json
from flask import request

from ihome import constants, db
from ihome import redis_store
from ihome.api_1_0 import api
from ihome.models import Area, House, Facility, HouseImage
from ihome.utils import image_storage
from ihome.utils.commons import login_required
from ihome.utils.response_code import RET


# @api.route("/house")
# def search_house():
#     aid = request
#    try:
#        house_query = House.query
#


# @api.route("/areas")
# def get_areas():
#     try:
#         redis_json_areas = redis_store.get("areas")
#     except Exception as e:
#         current_app.logger.error(e)
#         # return jsonify(errno=RET.DBERR,errmsg="获取失败"
#     if  redis_json_areas :
#         return jsonify(errno=RET.OK, errmsg="获取成功", data=json.loads(redis_json_areas))

@api.route('/areas')
def get_areas():
    """
    1.获取城区信息
    2.将城区信息转成字典列表
    3.返回
    :return:
    """

    # 0.先从redis中获取
    try:
        redis_json_areas = redis_store.get("areas")
    except Exception as e:
        current_app.logger.error(e)
        # return jsonify(errno=RET.DBERR,errmsg="获取失败")

    if redis_json_areas:
        return jsonify(errno=RET.OK, errmsg="获取成功", data=json.loads(redis_json_areas))

    try:
        areas = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询失败")

    areas_list = []
    for area in areas:
        areas_list.append(areas.to_dict())

    try:
        redis_store.set("areas", json.dumps(areas_list), constants.AREA_INFO_REDIS_EXPIRES)


    except Exception as e:
        current_app.logger.error(e)
        # return jsonify(errno=RET.DBERR,errmsg="存储失败")


        # 4.返回
    return jsonify(errno=RET.OK, errmsg="获取成功", data=areas_list)


@api.route("/houses", method=["POST"])
@login_required
def send_house_basic_info():
    title = request.json.get("title")
    price = request.json.get("price")
    area_id = request.json.get("area_id")
    address = request.json.get("address")
    room_count = request.json.get("room_count")
    acreage = request.json.get("acreage")
    unit = request.json.get("unit")
    capacity = request.json.get("capacity")
    beds = request.json.get("beds")
    deposit = request.json.get("deposit")
    min_days = request.json.get("min_days")
    max_days = request.json.get("max_days")
    facilities = request.json.get("facility")  # 格式:[1,

    if not all(
            [title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    house = House()
    house.title = title
    price = request.json.get("price")
    area_id = request.json.get("area_id")
    address = request.json.get("address")
    room_count = request.json.get("room_count")
    acreage = request.json.get("acreage")
    unit = request.json.get("unit")
    capacity = request.json.get("capacity")
    beds = request.json.get("beds")
    deposit = request.json.get("deposit")
    min_days = request.json.get("min_days")
    max_days = request.json.get("max_days")
    facilities = request.json.get("facility")  # 格式:[1,2,3,4]

    # 2.校验参数,基本信息校验
    if not all(
            [title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 3.创建房屋对象
    house = House()

    # 4.设置房屋对象的数据
    house.title = title
    house.price = price
    house.area_id = area_id
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days
    facility_list = Facility.query.filter(Facility.id in (facilities)).all()
    house.facilities = facility_list
    house.user_id = g.user_id
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存异常")

        # 7.返回
    return jsonify(errno=RET.OK, errmsg="发布成功", data={"house_id": house.id})


@api.route("/houses/<int:housde_id>/image", method=["POST"])
def send_house_image_info(house_id):
    image_data = request.files.get("house_image").read()
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询异常")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="该房屋不存在")
    try:
        image_name = image_storage(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="七牛云异常")

    if not house.index_image_url:
        house.index_image_url = image_name

    house_image = HouseImage()
    house_image.house_id = house_id
    house_image.url = image_name

    try:
        db.session.add(house_image)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="图片上传异常")


@api.route("/hoouses/<int:house_id>")
def get_house_detail(house_id):
    try:
        redis_house_detail = redis_store.get("house_detail:%s" % house_id)
    except:
        current_app.logger.error(e)
        # return jsonify(errno=RET.DBERR,errmsg="获取缓存异常")

        if redis_house_detail:
            return jsonify(errno=RET.OK, errmsg="获取成功", data={"house": json.loads(redis_house_detail)})
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询异常")
    if not house:
        return jsonify(errno=RET.NODATA, errmsg="该房屋不存在")


    try:
        redis_store.set("house_detail:%s"%house_id,json.dump(house.to_full_dict(),constants.HOUSE_DETAIL_REDIS_EXPIRE_SECOND))

    except Exception as e:
        current_app.logger.error(e)
        # return jsonify(errno=RET.DBERR,errmsg="缓存异常")
    return jsonify(errno=RET.OK,errmsg="获取成功",data={"house":house.to_full_dict()})

@api.route("/house/index")
def get_index_house():
    houses=None
    try:
        houses=House.query.oder_by(House.order_count.desc()).limit(constants.HOME_PAGE_MAX_HOUSES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询异常")
    house_list =[]
    for house in houses:
        house_list.append(house.to_basic_dict())
    return jsonify(errno=RET.OK, errmsg="获取成功", data=house_list)
