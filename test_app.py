import unittest
from json import loads
from datetime import datetime
from app import create_app
from db import db
from test_data_factory import ActorFactory, MovieFactory

class CastingAgencyTestCase(unittest.TestCase):
  """This class represents the actor test case"""

  def setUp(self):
    """Define test variables and initialize app."""
    db_user = 'postgres'
    db_password = 'password'
    db_host = 'localhost:5432'
    db_name = 'castingagencytest'
    self.db_path = 'postgresql://{}:{}@{}/{}'.format(db_user, db_password, db_host, db_name)

    app = create_app(db_path=self.db_path, drop_db=True)

    self.app = app
    self.client = self.app.test_client

  def tearDown(self):
    """Executed after reach test"""
    with self.app.app_context():
      db.session.rollback()
      pass

  #  ------------------------------------------------------------------------
  #  Actors
  #  ------------------------------------------------------------------------
  def test_get_actors(self):
    """Tests getting the actors"""
    num_actors_to_test = 10
    with self.app.app_context():
      ActorFactory.create_batch(num_actors_to_test)
      db.session.commit()

    res = self.client().get('/actors')
    data = loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertNotIn('error', data)
    # populated list
    actors = data['actors']
    self.assertEqual(len(actors), num_actors_to_test)

  def test_get_actor(self):
    """Tests getting an individual actor"""
    # creating multiple actors, and picking a specific one
    expected_id = 2
    expected_name = 'Morgan Freeman'
    expected_birthdate = 'Tue, 01 Jun 1937 00:00:00 GMT'

    with self.app.app_context():
      ActorFactory.create(name='Nicolas Cage', birthdate='Tue, 07 Jan 1964 00:00:00 GMT')
      ActorFactory.create(name=expected_name, birthdate=expected_birthdate)
      ActorFactory.create(name='Random Extra', birthdate=datetime.now())
      db.session.commit()

    res = self.client().get('actors/{}'.format(expected_id))
    data = loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertNotIn('error', data)
    actor = data['actor']
    # expected actor
    self.assertEqual(actor, { 'id': expected_id, 'name': expected_name, 'birthdate': expected_birthdate })

  #  ------------------------------------------------------------------------
  #  Movies
  #  ------------------------------------------------------------------------
  def test_get_movies(self):
    """Tests getting the movies"""

    num_movies_to_test = 10
    with self.app.app_context():
      MovieFactory.create_batch(num_movies_to_test)
      db.session.commit()

    res = self.client().get('/movies')
    data = loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertNotIn('error', data)
    # populated list
    movies = data['movies']
    self.assertEqual(len(movies), num_movies_to_test)

  def test_get_movie(self):
    """Tests getting an individual movie"""
    # creating multiple movies, and picking a specific one
    expected_id = 2
    expected_title = 'Driving Miss Daisy'
    expected_description = ('An old Jewish woman and her African-American chauffeur'
                            'in the American South have a relationship that grows'
                            'and improves over the years.')
    with self.app.app_context():
      MovieFactory.create(title='Con Air', description=(
        'Newly-paroled ex-con and former U.S. Ranger Cameron Poe finds'
        'himself trapped in a prisoner-transport plane when the passengers'
        'seize control.'))
      MovieFactory.create(title=expected_title, description=expected_description)
      MovieFactory.create(title='Random Movie', description='This is a random description.')
      db.session.commit()

    res = self.client().get('movies/{}'.format(expected_id))
    data = loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertNotIn('error', data)
    movie = data['movie']
    # expected movie
    self.assertEqual(movie, { 'id': expected_id, 'title': expected_title, 'description': expected_description })

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
