import unittest
from app import create_app
import json

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
      self.app.db.session.close()
      pass

  #  ------------------------------------------------------------------------
  #  Actors
  #  ------------------------------------------------------------------------
  def test_get_actors(self):
    """Tests getting the actors"""
    res = self.client().get('/actors')
    print(res)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertNotIn('error', data)
    # populated list
    actors = data['actors']
    self.assertEqual(actors, [])

  #  ------------------------------------------------------------------------
  #  Movies
  #  ------------------------------------------------------------------------
  def test_get_movies(self):
    """Tests getting the movies"""
    res = self.client().get('/movies')
    print(res)
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertNotIn('error', data)
    # populated list
    movies = data['movies']
    self.assertEqual(movies, [])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
