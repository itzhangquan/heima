from unittest import TestCase
from flask import json
from qq import app

class LoginTest():
    def setUp(self):
        self.client = app.test_client()
        app.testing=True
    def test_login_func(self):
        response=self.client.post("/login",data={"username":"","password":"aaaa"})
        json_data =response.data
        dict_data =json.loads(object)
        self.assertin("code",dict_data)
        self.asserEqual(dict_data["code"],1,"code的值必须等于１")

    def test_login_func_correct(self):
        # 1.获取测试客户端
        # client = app.test_client()

        # 2.发送请求
        response = self.client.post("/login", data={"username": "admin", "password": "123"})

        # 3.解析数据
        json_data = response.data
        dict_data = json.loads(json_data)

        # 4.校验
        self.assertIn("code", dict_data)
        # self.assertEqual(dict_data["code"],2)
        self.assertEqual(dict_data["code"], 0)
