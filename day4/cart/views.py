#coding:utf8
from flask import render_template
from . import  cart
#2.使用蓝图对象装饰视图函数
@cart.route('/cart')
def get_cart_info():

    return "get cart infomation"


@cart.route('/price')
def get_cart_price():

    return render_template("cart.html")
