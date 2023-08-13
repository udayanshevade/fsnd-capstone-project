from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values


db = SQLAlchemy()


def get_db_path():
    config = dotenv_values(".env")
    db_user = config.get('DB_USER', 'postgres')
    db_password = config.get('DB_PASSWORD', 'password')
    db_host = config.get('DB_HOST', 'localhost:5432')
    db_name = config.get('DB_NAME', 'castingagency')
    db_path = "postgresql://{}:{}@{}/{}".format(
        db_user,
        db_password,
        db_host,
        db_name
    )
    return db_path


def configure_app(app, db_path: str = get_db_path()):
    """Configures the app with the provided settings"""
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path


def setup_db(app, db_path: str = get_db_path(), drop_db: bool = False):
    """Initialize the database using the provided app instance and options"""
    configure_app(app, db_path=db_path)

    app.db = db
    db.app = app
    db.init_app(app)

    with app.app_context():
        if drop_db:
            db.drop_all()
        db.create_all()
