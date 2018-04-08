from flask_script import Manager
from forum import app
# from db_scripts import dbmanager
from flask_migrate import MigrateCommand, Migrate
from exts import db
from models import User

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()