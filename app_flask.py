import os
from flask_migrate import Migrate
import click
from flask import Flask
from src.manage import app
from src.database import db
from src.database.seed import Seed

migrate = Migrate(app, db)

def runserver():
    app.run(host='0.0.0.0', port=int(os.getenv('APP_PORT', 5000)))

@app.cli.command("seed")
# @click.argument("name")
def seed():
    seed = Seed()
    # seed.seed_user_role()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('APP_PORT', 5000)))
