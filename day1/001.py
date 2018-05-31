# coding:utf8

from flask import Flask
from flask import json
from flask import redirect
from werkzeug.routing import BaseConverter

app = Flask(__name__)
print app.static_url_path
print app.static_folder
print app.template_folder


class myconverter(BaseConverter):
    def __init__(self, url_map, regex):
        super(myconverter, self).__init__(url_map)
        self.regex = regex

    def to_python(self, value):
        return "1" + value


app.url_map.converters["re"] = myconverter


@app.route('/<re(r"\d"):num1>', methods=["POST"])
def helloworld(num1):
    return redirect("/jianghuan%s" % num1)


@app.route('/jianghuan13', methods=["POST", "GET"])
def jianghuan():
    dict = {"name": "xiaoming"}
    jsonstr = json.dumps(dict)
    return jsonstr


if __name__ == '__main__':
    app.run(debug=True)
