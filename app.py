from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from db import db, setup_db
from actors.routes import actors_blueprint
from movies.routes import movies_blueprint


def create_app(db_path: str = None, drop_db: bool = False):
    # create and configure the app
    app = Flask(__name__)

    # setup middleware
    CORS(app)

    # initialize db
    setup_db(app, db_path=db_path, drop_db=drop_db)

    # register routes
    app.register_blueprint(actors_blueprint)
    app.register_blueprint(movies_blueprint)

    return app


def init_app():
    app = create_app()
    Migrate(app, db)
    app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    init_app()
