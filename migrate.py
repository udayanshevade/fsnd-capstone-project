from flask_migrate import Migrate

migrate = Migrate()


def setup_migrations(app):
  migrate.init_app(app)
