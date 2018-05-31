#coding:utf8
from flask import Blueprint
cart=Blueprint("cart",__name__,url_prefix="/cart",template_folder="xxx")
from . import  views