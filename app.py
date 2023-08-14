from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from db import db, setup_db, get_db_path
from migrate import setup_migrations
from actors.routes import actors_blueprint
from movies.routes import movies_blueprint
from errors import app_error_handling


def init_app(db_path: str = None, drop_db: bool = False):
    # create and configure the app
    app = Flask(__name__)

    # setup middleware
    CORS(app)

    # initialize db
    setup_db(app, db_path=db_path, drop_db=drop_db)

    setup_migrations(app)

    @app.route('/healthcheck', methods=['GET'])
    def healthcheck():
        return 'OK', 200

    # register routes
    app.register_blueprint(actors_blueprint)
    app.register_blueprint(movies_blueprint)

    app_error_handling(app)

    return app


def create_app():
    db_path = get_db_path()
    app = init_app(db_path=db_path)
    Migrate(app, db)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True)
