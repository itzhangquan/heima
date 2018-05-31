# coding:utf8
from flask import Flask
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:mysql@localhost:3306/person'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)


class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    age = db.Column(db.Integer)
    money = db.Column(db.Integer)


@app.route('/')
def index():
    return "helloworld"

zhangquan = Person(name="zhangsan",age=18,money="1000")
db.session.add(zhangquan)
db.session.commit()

if __name__ == "__main__":
    manager.run()
    db.drop_all()
    db.create_all()
