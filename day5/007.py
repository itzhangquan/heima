#coding:utf8
"""
二维码的获取流程:
1. 获取accesstoken(上份代码已完成)

2. 发送请求,获取ticket
地址:https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=TOKEN
方式:POST
请求体:{"expire_seconds": 604800, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": 123}}}
返回:
成功:
ticket:
expire_seconds:
url:

失败:
{"errcode":40013,"errmsg":"invalid appid"}

3. 通过ticket换取二维码
发送: https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=TICKE
方式:GET

"""""
from flask import json

from ww import Accesstoken
from flask import Flask
import urllib2
app=Flask(__name__)
@app.route('/qr_code/<int:id>')
def index():
    accwsstoken = Accesstoken.get_accesstoken()

    url ="https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s"
    dict_data =  {"expire_seconds": 604800, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": id}}}
    request＿obj =urllib2.Request(url,data=json.dumps(dict_data))
    json_data = urllib2.urlopen(request＿obj).read()


    dict_data=json_data.loads(json_data)

    if "errcode" in dict_data:
        return "获取二维码失败"

    qr_code_url= "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s"%dict_data.get("ticket")
    return "<img src='%s'>"%qr_code_url
if __name__ == '__main__':
    app.run(debug=True)
