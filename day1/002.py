#coding=utf-8
from  flask import  Flask
from flask import abort

app = Flask(__name__)
@app.route('/')
def exceotion():
    # abort(404)
    1/0
    return "a"
@app.errorhandler(ZeroDivisionError)
def eee(e):
    print e
    return "0不能为除数"
if __name__ == '__main__':
    app.run()