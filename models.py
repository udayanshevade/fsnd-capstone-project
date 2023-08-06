from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values

db = SQLAlchemy()

config = dotenv_values(".env")

db_user = getattr(config, 'DB_USER', 'postgres')
db_password = getattr(config, 'DB_PASSWORD', 'password')
db_host = getattr(config, 'DB_HOST', 'localhost')
db_name = getattr(config, 'DB_NAME', 'castingagency')
db_path = "postgresql://{}:{}@{}/{}".format(db_user, db_password, db_host, db_name)

def configure_app(app, db_path:str=db_path):
  """Configures the app with the provided settings"""
  app.config["SQLALCHEMY_DATABASE_URI"] = db_path


def setup_db(app, db_path:str=db_path, drop_db:bool=False):
  """Initialize the database using the provided app instance and options"""
  configure_app(app, db_path=db_path)

  app.db = db
  db.app = app
  db.init_app(app)

  with app.app_context():
    if drop_db: db.drop_all()
    db.create_all()

class Movie(db.Model):
  __tablename__ = "movies"
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String())
  description = db.Column(db.Text())
  def __repr__(self):
        return f'<Movie ID: {self.id}, title: {self.title}, complete: {self.description}>'

class Actor(db.Model):
  __tablename__ = 'actors'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  birthdate = db.Column(db.Date)
  def __repr__(self):
        return f'<Actor ID: {self.id}, name: {self.name}, birthdate: {self.birthdate}>'