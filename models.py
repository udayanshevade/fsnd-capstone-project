from sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import dotenv_values

db = SQLAlchemy()

config = dotenv_values(".env")

database_host = config['DATABASE_HOST']
database_name = config['DATABASE_NAME']
database_path = "postgresql://{}/{}".format(database_host, database_name)

def setup_db(app, database_path = database_path):
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  db.app = app
  db.init_app(app)
  db.create_all()

migrate = Migrate(db.app, db)

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