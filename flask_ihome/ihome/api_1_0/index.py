#coding=utf-8
import logging

from flask import current_app
from flask import session

from . import api
from ihome import models


@api.route('/', methods=["GET", "POST"])
def index():
    session["name"] = "zhangsan"
    logging.debug("调试信息")
    logging.info("详细信息")
    logging.warn("警告信息")
    logging.error("错误信息")

    current_app.logger.debug("===调试信息")
    current_app.logger.info("===详细信息")
    current_app.logger.warning("===警告信息")
    current_app.logger.error("===错误信息")
    return "helloworld"
