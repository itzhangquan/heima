#coding:utf8
from flask import Flask
from user import get_user

app = Flask(__name__)
app.route("/user")(get_user)

@app.route('/product')
def get_product():
    return "获取商品信息"

if __name__ == '__main__':
    print app.url_map
    app.run(debug=True)