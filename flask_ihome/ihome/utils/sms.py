#coding:utf8
from ihome.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

# 说明：主账号，登陆云通讯网站后，可在控制台首页中看到开发者主账号ACCOUNT SID。
accountSid = '8a216da8635da72901635dc414f50045';

# 说明：主账号Token，登陆云通讯网站后，可在控制台首页中看到开发者主账号AUTH TOKEN。
accountToken = '2147e72bdff94698b6a63ac59a82318d';

# 请使用管理控制台中已创建应用的APPID。
appId = '8a216da8635da72901635dc41553004b';

# 说明：请求地址，生产环境配置成app.cloopen.com。
serverIP = 'app.cloopen.com';

# 说明：请求端口 ，生产环境为8883.
serverPort = '8883';

softVersion = '2013-12-26';  # 说明：REST API版本号保持不变。

#将短信发送的过程使用单利进行封装
#单利的写法有很多写法!开发中掌握一种就可以,但是面试会问很多种
class CCP(object):

#测试代码
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance=super(CCP,cls).__new__(cls)
            cls.__instance.rest=REST(serverIP,serverPort,softVersion)
            cls.__instance.rest.setAccount(accountSid,accountToken)
            cls.__instance.rest.setAppId(appId)
            return cls.__instance
        else:
            return cls.__instance

    def sendTemplateSMS(self,to,datas,tempId):
        result =self.rest.sendTemplateSMS(to,datas,tempId)

        if result["statusCode"]=="000000":
            return 0
        else:
            return -1

