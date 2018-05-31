#coding:utf8
"""
功能: 处理语音消息,并将语音消息解析成文本返回

分析:
1. 获取请求, post
2. 解析参数xml格式, 解析成字典
3. 封装成返回回去的数据

"""""
import time
import xmltodict
from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)

token = "python7"

@app.route('/wechat8001',methods=["GET","POST"])
def index():

    #1.获取参数
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    echostr = request.args.get("echostr")

    #2.将token、timestamp、nonce三个参数进行字典序排序
    params = [token,timestamp,nonce]
    params.sort()

    #3.将三个参数字符串拼接成一个字符串进行sha1加密
    params_str = "".join(params)
    signature2 = hashlib.sha1(params_str).hexdigest()

    #4.开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
    if request.method == "GET":
        if signature == signature2:
            return echostr
        else:
            return ""
    else:

        #获取用户的数据
        xml_data = request.data

        #将xml转成字典
        dict_data = xmltodict.parse(xml_data).get("xml")

        #取出消息类型
        msg_type = dict_data.get("MsgType")

        #判断消息类型
        if msg_type == "text": #文本消息

          #封装返回的字典
            resp_dict = {
                "ToUserName":dict_data.get("FromUserName"),
                "FromUserName":dict_data.get("ToUserName"),
                "CreateTime":time.time(),
                "MsgType":"text",
                "Content":dict_data.get("Content","")
            }

            #根节点包装成xml
            xml_dict = {"xml":resp_dict}

            #将字典转成xml返回给微信服务器
            return xmltodict.unparse(xml_dict)

        elif msg_type == "voice": #语音消息

            print dict_data.get("Recognition")

            # 封装返回的字典
            resp_dict = {
                "ToUserName": dict_data.get("FromUserName"),
                "FromUserName": dict_data.get("ToUserName"),
                "CreateTime": time.time(),
                "MsgType": "text",
                "Content": dict_data.get("Recognition", u"无法识别")
            }

            # 根节点包装成xml
            xml_dict = {"xml": resp_dict}

            # 将字典转成xml返回给微信服务器
            return xmltodict.unparse(xml_dict)


        else: #其他类型消息
            # 封装返回的字典
            resp_dict = {
                "ToUserName": dict_data.get("FromUserName"),
                "FromUserName": dict_data.get("ToUserName"),
                "CreateTime": time.time(),
                "MsgType": "text",
                "Content": dict_data.get(u"么么哒", "")
            }

            # 根节点包装成xml
            xml_dict = {"xml": resp_dict}

            # 将字典转成xml返回给微信服务器
            return xmltodict.unparse(xml_dict)


if __name__ == "__main__":
    app.run(port=8001,debug=True)
