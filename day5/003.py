import time
from flask import Flask
import hashlib
import xmltodict

from flask import request

app = Flask(__name__)

token = "python7"


@app.route('/wechat8001')
def index():
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    echostr = request.args.get("echostr")

    params = [token, timestamp, nonce]
    params.sort()

    params_str = "".join(params)
    signature2 = hashlib.sha1(params_str).hexdigest()

    if request.method == "GET":
        if signature == signature2:
            return echostr
        else:
            return ""
    else:
        xml_data = request.data
        dict_data = xmltodict.parse(xml_data).get("xml")
        msg_type = dict_data.get("msg_type")
        if msg_type == "text":
            resp_dict = {
                "ToUserName": "FromUserName",
                "FromUSerName": "ToUserName",

                "CreateTime": time.time(),
                "MsgType": "text",
                "content": dict_data.get("content", "")
            }
            return xmltodict.unparse({"xml": msg_type})

        else:

            resp_dict = {
                "ToUserName": "FromUserName",
                "FromUSerName": "ToUserName",

                "CreateTime": time.time(),
                "MsgType": "text",
                "content": dict_data.get(u"么么打", "")
            }
            return xmltodict.unparse({"xml": msg_type})

if __name__ == '__main__':
    app.run(debug=True)
