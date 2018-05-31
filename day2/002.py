#coding:utf8
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/index')
def index():
    str = u"蒋欢好美"
    tuple = (1,2,3)
    dict = {"lover":"jianghuan","name":13}
    list=[1,1,3,4,5,6]
    return render_template("file01.html",str=str,tuple=tuple,dict=dict,list=list)
if __name__ == '__main__':
    app.run()