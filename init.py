from flask_cors import CORS
from db import setup_db
from migrate import setup_migrations
from actors.routes import actors_blueprint
from movies.routes import movies_blueprint
from errors import app_error_handling

def init_app(app, db_path: str = None, drop_db: bool = False):
    """Configure the app"""

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