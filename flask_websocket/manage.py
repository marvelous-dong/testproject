from flask_script import Manager, Server
from app import app
from flask_migrate import Migrate, MigrateCommand
from database.exts import db
from database.models import User
from database.models import Classes


manager = Manager(app)
Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)
manager.add_command("start", Server(port=9527, use_debugger=True))

if __name__ == '__main__':
    manager.run()
