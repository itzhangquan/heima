#coding=utf-8
from functools import wraps

from flask import g, jsonify
from flask import session
from werkzeug.routing import BaseConverter

from ihome.utils.response_code import RET


class RegexConverter(BaseConverter):
    def __init__(self,url_map,regex):
        super(RegexConverter,self).__init__(url_map)
        self.regex=regex

#
# def login_required(view＿func):
#     @wraps(view＿func)
#     def wrapper(*args,**kwargs):
#         g.user_id = session.get("user_id")
#
#         if g.user_id:
#             return view＿func(*args,**kwargs)
#         else:
#             return jsonify(errno=RET.NODATA,errmsg="该用户尚未登录")
#     return wrapper
def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args,**kwargs):
        #取出session中的编号
        g.user_id = session.get("user_id")

        #判断g对象中的编号
        if g.user_id:
            return view_func(*args,**kwargs)
        else:
            return jsonify(errno=RET.NODATA,errmsg="该用户尚未登录")

    return wrapper