from flask import Flask
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):
  # create and configure the app
  _app = Flask(__name__)
  setup_db(_app)
  CORS(_app)

  return _app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)