import redis
from flask import Flask
from flask.ext.session import Session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import CSRFProtect

from config import config_dict
from ihome.utils.commons import RegexConverter

db = SQLAlchemy()

redis_store = None
def create_app(config_name):
    app = Flask(__name__)
    config = config_dict.get(config_name)
    app.config.from_object(config)
    db = SQLAlchemy(app, "db")
    db.init_app(app)
    global  redis_store
    redis_store = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT)

    Session(app)
    CSRFProtect(app)
    app.url_map.converters["re"] = RegexConverter

    from ihome.api_1_0 import api
    app.register_blueprint(api)
    from ihome.web_html import web_html
    app.register_blueprint(web_html)
    return app
