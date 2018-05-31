#coding:utf8
from flask import Flask
from flask import flash
from flask import render_template
from flask import session

app = Flask(__name__)
app.config["SECRET_KEY"]="dfevghnjyujtyrgvfcsdxaxAGHR"
@app.route('/index1')
def index1():
    session["name"]= "zhangsan"
    return render_template("01.html")
@app.route('/index2')
def index2():
    flash(u"人生苦短")
    flash(u"我用python")
    return "helloworls"

if __name__ == '__main__':

    app.run(debug=True)