from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from db import get_db_path
from init import init_app
from dotenv import load_dotenv

def create_app():
    db_path = get_db_path()
    app = Flask(__name__)
    init_app(app=app, db_path=db_path)
    return app

app = create_app()

if __name__ == '__main__':
    load_dotenv()
    app.run(host='0.0.0.0', port=8080, debug=True)
