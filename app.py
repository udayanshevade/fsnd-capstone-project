from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

def create_app(test_config=None):
  # create and configure the app
  _app = Flask(__name__)
  _app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/castingagency'
  CORS(_app)

  return _app

app = create_app()

db = SQLAlchemy(app)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)