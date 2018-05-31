from flask import  Flask
from flask import render_template

app=Flask(__name__)
@app.template_filter("myfilter")
def get_element(ls):
    return ls[::2]
# app.add_template_filter(get_element,"myfilter")
@app.route('/index')
def index():
    return render_template("file3.html",mylist =[x for x in range(0,200)])
app.run(debug=True)