from os import getenv
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def build_db_path(db_dialect, db_user, db_password, db_host, db_name):
    db_path = "{}://{}:{}@{}/{}".format(
        db_dialect,
        db_user,
        db_password,
        db_host,
        db_name
    )
    return db_path


def get_db_path():
    db_dialect = getenv('DB_DIALECT', 'postgresql')
    db_user = getenv('DB_USER', 'postgres')
    db_password = getenv('DB_PASSWORD', 'password')
    db_host = getenv('DB_HOST', 'localhost:5432')
    db_name = getenv('DB_NAME', 'castingagency')
    return build_db_path(db_dialect, db_user, db_password, db_host, db_name)


def configure_app(app, db_path: str):
    """Configures the app with the provided settings"""
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path


def setup_db(app, db_path: str, drop_db: bool = False):
    """Initialize the database using the provided app instance and options"""
    configure_app(app, db_path=db_path)

    app.db = db
    db.app = app
    db.init_app(app)

    with app.app_context():
        if drop_db:
            db.drop_all()
        db.create_all()
