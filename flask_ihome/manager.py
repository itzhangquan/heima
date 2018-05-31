#coding=utf8

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

from ihome import create_app,db

app =create_app("develop")


manager=Manager(app)
Migrate(app,db)
manager.add_command("db",MigrateCommand)
if __name__ == '__main__':
    manager.run()
    db.drop_all()
    db.create_all()