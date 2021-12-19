import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.manage import app
from src.database import db
from src.database.seed import Seed

migrate = Migrate(app, db)
manager = Manager(app)

@manager.command
def runserver():
    app.run(host='0.0.0.0', port=int(os.getenv('APP_PORT', 5000)))

manager.add_command('db', MigrateCommand)

@manager.command
def seed():
    seed = Seed()
    seed.seed_user_role()


if __name__ == "__main__":
    manager.run()
