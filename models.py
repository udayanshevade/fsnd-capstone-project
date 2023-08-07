from db import db

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
