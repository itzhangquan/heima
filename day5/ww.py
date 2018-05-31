
#coding:utf8
"""
accesstoken: 是微信服务器识别我们开发者的凭据, 通过它我们可以获取比如:二维码,卡券,微信小店,广告推送等功能.

获取流程:
1. 发送请求:https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
    参数: APPID,APPSECRET

    请求方式: GET

2.返回
正确:
{
    "access_token":"ACCESS_TOKEN",
    "expires_in":7200
}

错误:
{
    "errcode":40013,
    "errmsg":"invalid appid"
}"""""
import time
import urllib2

from flask import json
appID="wx1322bc2a5eaa004c"
appsecrect="b544dcb267b240c87d0fd86fc62ea95a"

class Accesstoken(object):
    __accesstoken={
        "access_token":"",
        "expires_in":7200,
        "update_time":time.time()
    }
    @classmethod
    def get_accesstoken(cls):
        access_token =cls.__accesstoken.get("access_token")
        isExpire =time.time()-cls.__accesstoken.get("update_time")<cls.get_accesstoken("expire_time")
        if access_token and isExpire:
            return access_token

        else:
            url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(appID,appsecrect)
            json_data = urllib2.urlopen(url).read()
            dict_data = json.loads(json_data)
            if "errcode" in dict_data:
                return "获取失败"
            else:
                cls.__accesstoken["access_token"]=dict_data.get("access_token")
                cls.__accesstoken["expires_in"]=dict_data.get("expire_in")
                cls.__accesstoken["update_time"]=time.time()
                return cls.__accesstoken["access_token"]

