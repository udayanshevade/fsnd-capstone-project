import factory
from models import Actor, Movie
from db import db

class ActorFactory(factory.alchemy.SQLAlchemyModelFactory):
  """Factory for generating mocked Actor instances for testing"""
  class Meta:
    model = Actor
    sqlalchemy_session = db.session

  name = factory.Faker('name')
  birthdate = factory.Faker('date')

class MovieFactory(factory.alchemy.SQLAlchemyModelFactory):
  """Factory for generating mocked Movie instances for testing"""
  class Meta:
    model = Movie
    sqlalchemy_session = db.session

  title = factory.Faker('sentence', nb_words=3)
  description = factory.Faker('sentence')
