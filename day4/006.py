#coding:utf8
def div(num1,num2):
    assert isinstance(num1,int),Exception("num1必须是一个整数")
    assert isinstance(num2,int),Exception("num2必须是一个整数")

    return num1/num2

print div(100,0.5)