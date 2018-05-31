#coding:utf8
import redis



class BaseConfig(object):

    SECRET_KEY = "jdhufbredjwbdi"
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost:3306/flask_ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 2

class DevelopConfig(BaseConfig):
    DEBUG = True

class ProductConfig(BaseConfig):
    pass


config_dict={
    "develop":DevelopConfig,
    "product":ProductConfig

}
