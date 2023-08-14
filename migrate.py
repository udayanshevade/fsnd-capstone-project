from flask_migrate import Migrate
from db import db

migrate = Migrate()


def setup_migrations(app):
  migrate.init_app(app, db)
