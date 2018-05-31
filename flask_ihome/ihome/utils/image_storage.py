#coding=utf-8
from qiniu import Auth,put_file,etag,put_data
access_key = 'v3n5FPnRvLujRroKe3X9FxjMSgtWCmMWBeharusu'
secret_key=  'd3uJUlaQ9iKh0b5XkhU-Tlx5hjrDiWDDeHA4xotw'

q=Auth(access_key,secret_key)

bucket_name ="ihome"
token = q.upload_token(bucket_name,None,3600)

def image_storage(image_data):
    ret,info= put_data(token,None,image_data)

    if info.status_code ==200:
        return  ret.get("key")
    else:
        return ""

if __name__ == '__main__':
    with open("./22.png") as file:
        image_storage(file.read())

