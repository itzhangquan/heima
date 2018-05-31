from flask import Flask,Blueprint

pro=Blueprint("product",__name__)

@pro.route('/get_product')
def get_product():
    return "this is product"