import unittest
from flask import Flask
from json import loads
from datetime import datetime
from init import init_app
from db import db
from test_data_factory import ActorFactory, MovieFactory
from dotenv import dotenv_values

birthdate_format = '%a, %d %b %Y %H:%M:%S GMT'

config = dotenv_values(".env")


def get_headers_for_casting_assistant():
    """Test auth token for read-only endpoints"""
    auth_token = config.get('CASTING_ASSISTANT_AUTH_TOKEN', '')
    return {
        'Authorization': 'Bearer ' + auth_token
    }


def get_headers_for_casting_director():
    """Test auth token: CRUD for actors, RU for movies"""
    auth_token = config.get('CASTING_DIRECTOR_AUTH_TOKEN', '')
    return {
        'Authorization': 'Bearer ' + auth_token
    }


def get_headers_for_executive_producer():
    """
    Test auth token with all permissions
    (using this as default for testing endpoints)
    """
    auth_token = config.get('EXECUTIVE_PRODUCER_AUTH_TOKEN', '')
    return {
        'Authorization': 'Bearer ' + auth_token
    }


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the actor test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        db_user = 'postgres'
        db_password = 'password'
        db_host = 'localhost:5432'
        db_name = 'castingagencytest'
        self.db_path = 'postgresql://{}:{}@{}/{}'.format(
            db_user,
            db_password,
            db_host,
            db_name)

        app = Flask(__name__)

        init_app(app, db_path=self.db_path, drop_db=True)

        self.app = app
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            db.session.rollback()
            pass

    #  ------------------------------------------------------------------------
    #  Auth errors
    #  ------------------------------------------------------------------------
    def test_auth_missing_token(self):
        """Tests that auth error handling checks for header"""
        res = self.client().get('/actors')
        data = loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is required')

    def test_auth_invalid_token(self):
        """Tests that auth error handling checks for valid header"""
        invalid_headers = {'Authorization': 'Bearer sus'}
        res = self.client().get('/actors', headers=invalid_headers)
        data = loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization malformed')

    def test_expired_token(self):
        """Tests that token expiry is checked"""
        expired_auth_token = config.get('EXPIRED_AUTH_TOKEN')
        invalid_headers = {
            'Authorization': f'Bearer {expired_auth_token}'
        }
        res = self.client().get('/actors', headers=invalid_headers)
        data = loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Token has expired')

    #  ------------------------------------------------------------------------
    #  Actors
    #  ------------------------------------------------------------------------
    def test_get_actors(self):
        """Tests getting the actors"""
        num_actors_to_test = 10
        with self.app.app_context():
            ActorFactory.create_batch(num_actors_to_test)
            db.session.commit()

        res = self.client().get(
            '/actors',
            headers=get_headers_for_executive_producer()
        )
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
            ActorFactory.create(
                name='Nicolas Cage',
                birthdate='Tue, 07 Jan 1964 00:00:00 GMT'
            )
            ActorFactory.create(
                name=expected_name,
                birthdate=expected_birthdate
            )
            ActorFactory.create(
                name='Random Extra',
                birthdate=datetime.now()
            )
            db.session.commit()

        res = self.client().get(
            f'actors/{expected_id}',
            headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotIn('error', data)
        actor = data['actor']
        # expected actor
        self.assertEqual(
            actor,
            {
                'id': expected_id,
                'name': expected_name,
                'birthdate': expected_birthdate,
            }
        )

    def test_get_actor_error_404(self):
        """Tests an error getting an actor"""
        out_of_range_id = 3
        with self.app.app_context():
            ActorFactory.create_batch(2)
            db.session.commit()

        res = self.client().get(
            f'actors/{out_of_range_id}',
            headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_update_actor(self):
        """Tests updating an existing actor"""
        with self.app.app_context():
            ActorFactory.create(
                name='Jamie Lee Curtis',
                birthdate='Sat, 22 Nov 1958 00:00:00 GMT')
            db.session.commit()

        id = 1
        expected_name = 'Lindsay Lohan'
        expected_birthdate = 'Wed, 02 Jul 1986 00:00:00 GMT'
        patch_data = {
            'name': expected_name,
            'birthdate': datetime.strptime(
                expected_birthdate,
                birthdate_format
            ).isoformat()
        }
        res = self.client().patch(
            f'actors/{id}',
            json=patch_data, headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotIn('error', data)
        actor = data['actor']
        self.assertEqual(
            actor,
            {
                'id': id,
                'name': expected_name,
                'birthdate': expected_birthdate
            }
        )

    def test_update_actor_error_422(self):
        """Tests an error while updating an actor"""
        with self.app.app_context():
            ActorFactory.create(
                name='Jamie Lee Curtis',
                birthdate='Sat, 22 Nov 1958 00:00:00 GMT')
            db.session.commit()
        id = 1
        patch_data = {
            'name': 'Lindsay Lohan',
            'birthdate': ''
        }
        res = self.client().patch(
            f'actors/{id}',
            json=patch_data,
            headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_create_actor(self):
        """Tests creating a new actor"""
        expected_name = 'Tommy Wiseau'
        expected_birthdate = 'Tue, 22 Nov 1955 00:00:00 GMT'
        post_data = {
            'name': expected_name,
            'birthdate': datetime.strptime(
                expected_birthdate,
                birthdate_format
            ).isoformat()
        }
        res = self.client().post(
            'actors',
            json=post_data,
            headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotIn('error', data)
        actor = data['actor']
        self.assertEqual(
            actor,
            {
                'id': 1,
                'name': expected_name,
                'birthdate': expected_birthdate,
            }
        )

    def test_create_actor_400(self):
        """Tests an error while creating an actor"""
        post_data = {
            'name': 'Chuck Norris',
        }
        res = self.client().post(
            'actors',
            json=post_data,
            headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        """Tests deleting a actor"""
        with self.app.app_context():
            ActorFactory.create(
                name='Arnold Schwarzenegger',
                birthdate='Wednesday, 30 Jul 1947 00:00:00 GMT'
            )
            ActorFactory.create(
                name='Tommy Wiseau',
                birthdate='Sat, 22 Nov 1955 00:00:00 GMT'
            )
            db.session.commit()
        id = 2
        res = self.client().delete(
            f'actors/{id}',
            headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotIn('error', data)
        removed = data['removed']
        self.assertEqual(removed, id)

    def test_delete_actor_404(self):
        """Tests an error while deleting an actor"""
        with self.app.app_context():
            ActorFactory.create()
            db.session.commit()
        out_of_range_id = 2
        res = self.client().delete(
            f'actors/{out_of_range_id}',
            headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    #  ------------------------------------------------------------------------
    #  Movies
    #  ------------------------------------------------------------------------
    def test_get_movies(self):
        """Tests getting the movies"""

        num_movies_to_test = 10
        with self.app.app_context():
            MovieFactory.create_batch(num_movies_to_test)
            db.session.commit()

        res = self.client().get(
            '/movies',
            headers=get_headers_for_executive_producer()
        )
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
        expected_description = ('An old Jewish woman and her African-American '
                                'chauffeur in the American South have a '
                                'relationship that grows and improves over '
                                'the years.')
        with self.app.app_context():
            MovieFactory.create(
                title='Con Air',
                description=(
                    'Newly-paroled ex-con and former U.S. Ranger Cameron Poe '
                    'finds himself trapped in a prisoner-transport plane '
                    'when the passengers seize control.'
                )
            )
            MovieFactory.create(
                title=expected_title,
                description=expected_description
            )
            MovieFactory.create(
                title='Random Movie',
                description='This is a random description.'
            )
            db.session.commit()

        res = self.client().get(
            f'movies/{expected_id}',
            headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotIn('error', data)
        movie = data['movie']
        # expected movie
        self.assertEqual(
            movie,
            {
                'id': expected_id,
                'title': expected_title,
                'description': expected_description
            }
        )

    def test_get_movie_error_404(self):
        """Tests an error getting an movie"""
        out_of_range_id = 3
        with self.app.app_context():
            MovieFactory.create_batch(2)
            db.session.commit()

        res = self.client().get(
            f'movies/{out_of_range_id}',
            headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_update_movie(self):
        """Tests updating an existing movie"""
        with self.app.app_context():
            MovieFactory.create(
                title='Dawn of the Dead',
                description=('During an escalating zombie epidemic, two '
                             'Philadelphia SWAT team members, a traffic '
                             'reporter and his TV executive girlfriend seek '
                             'refuge in a secluded shopping mall.')
            )
            db.session.commit()

        id = 1
        expected_title = 'Dawn of the Dead'
        expected_description = ('A nurse, a policeman, a young married '
                                'couple, a salesman and other survivors of a '
                                'worldwide plague that is producing '
                                'aggressive, flesh-eating zombies, take '
                                'refuge in a mega Midwestern shopping mall.')
        patch_data = {
            'title': expected_title,
            'description': expected_description
        }
        res = self.client().patch(
            f'movies/{id}',
            json=patch_data,
            headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotIn('error', data)
        movie = data['movie']
        self.assertEqual(
            movie,
            {
                'id': id,
                'title': expected_title,
                'description': expected_description
            }
        )

    def test_update_movie_error_404(self):
        """Tests an error while updating a movie"""
        with self.app.app_context():
            MovieFactory.create(
                title='Dawn of the Dead',
                description=('During an escalating zombie epidemic, two '
                             'Philadelphia SWAT team members, a traffic '
                             'reporter and his TV executive girlfriend seek '
                             'refuge in a secluded shopping mall.')
            )
            db.session.commit()
        out_of_range_id = 2
        patch_data = {
            'title': 'Sharknado',
            'description': ('When a freak hurricane swamps Los Angeles, '
                            "nature's deadliest killer rules sea, land, and "
                            'air as thousands of sharks terrorize the '
                            'waterlogged populace.')
        }
        res = self.client().patch(
            f'actors/{out_of_range_id}',
            json=patch_data,
            headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_movie(self):
        """Tests creating a new movie"""
        expected_title = 'The Room'
        expected_description = ("In San Francisco, an amiable banker's "
                                'seemingly perfect life is turned upside down '
                                'when his deceitful fiancée embarks on an '
                                'affair with his best friend.')
        post_data = {
            'title': expected_title,
            'description': expected_description
        }
        res = self.client().post(
            '/movies',
            json=post_data,
            headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotIn('error', data)
        movie = data['movie']
        self.assertEqual(
            movie,
            {
                'id': 1,
                'title': expected_title,
                'description': expected_description,
            }
        )

    def test_create_movie_400(self):
        """Tests an error while creating a movie"""
        post_data = {
            'title': 'Batgirl',
        }
        res = self.client().post(
            '/movies',
            json=post_data,
            headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        """Tests deleting a movie"""
        with self.app.app_context():
            MovieFactory.create(
                title='Dawn of the Dead',
                description=('During an escalating zombie epidemic, two '
                             'Philadelphia SWAT team members, a traffic '
                             'reporter and his TV executive girlfriend seek '
                             'refuge in a secluded shopping mall.')
                )
            MovieFactory.create(
                title='The Room',
                description=("In San Francisco, an amiable banker's seemingly "
                             "perfect life is turned upside down when his "
                             "deceitful fiancée embarks on an affair with his "
                             "best friend.")
            )
            db.session.commit()
        id = 2
        res = self.client().delete(
            f'movies/{id}',
            headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotIn('error', data)
        removed = data['removed']
        self.assertEqual(removed, id)

    def test_delete_movie_404(self):
        """Tests an error while deleting an movie"""
        with self.app.app_context():
            MovieFactory.create()
            db.session.commit()
        out_of_range_id = 2
        res = self.client().delete(
            f'movies/{out_of_range_id}',
            headers=get_headers_for_executive_producer()
        )
        data = loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    #  ------------------------------------------------------------------------
    #  RBAC tests
    #  ------------------------------------------------------------------------
    def test_assistant_role_can_get_data(self):
        """Tests that the assistant role has read permissions"""
        with self.app.app_context():
            ActorFactory.create()
            MovieFactory.create()
            db.session.commit()
        headers = get_headers_for_casting_assistant()
        actors_res = self.client().get('/actors', headers=headers)
        self.assertEqual(actors_res.status_code, 200)
        movies_res = self.client().get('/movies', headers=headers)
        self.assertEqual(movies_res.status_code, 200)

    def test_assistant_role_cannot_post_data(self):
        """
        Tests that the assistant role doesn't have permissions to post data
        """
        actor_data = {
            'name': 'Marlon Rando',
            'birthdate': datetime.strptime(
                'Tue, 01 Aug 2023 00:00:00 GMT',
                birthdate_format
            ).isoformat()
        }
        headers = get_headers_for_casting_assistant()
        actors_res = self.client().post(
            '/actors',
            json=actor_data,
            headers=headers
        )
        self.assertEqual(actors_res.status_code, 401)
        movie_data = {
            'title': 'Random',
            'description': 'This is a random movie'
        }
        movies_res = self.client().post(
            '/movies',
            json=movie_data,
            headers=headers
        )
        self.assertEqual(movies_res.status_code, 401)

    def test_director_role_can_crud_actor_data(self):
        """Tests that the director role has CRUD permissions for actor data"""
        with self.app.app_context():
            ActorFactory.create()
            db.session.commit()
        headers = get_headers_for_casting_director()

        read_res = self.client().get('/actors', headers=headers)
        self.assertEqual(read_res.status_code, 200)

        post_data = {
            'name': 'Marlon Rando',
            'birthdate': datetime.strptime(
                'Tue, 01 Aug 2023 00:00:00 GMT',
                birthdate_format
            ).isoformat()
        }
        post_res = self.client().post(
            '/actors',
            json=post_data,
            headers=headers
        )
        self.assertEqual(post_res.status_code, 200)

        patch_data = {
            'name': 'Marlin Rando',
            'birthdate': datetime.strptime(
                'Wed, 02 Aug 2023 00:00:00 GMT',
                birthdate_format
            ).isoformat()
        }
        patch_res = self.client().patch(
            '/actors/2',
            json=patch_data,
            headers=headers
        )

        self.assertEqual(patch_res.status_code, 200)

        delete_res = self.client().delete('/actors/1', headers=headers)
        self.assertEqual(delete_res.status_code, 200)

    def test_director_role_can_only_read_and_update_movie_data(self):
        """
        Tests that the director role has limited R+U permissions for movies
        """
        with self.app.app_context():
            MovieFactory.create(
                title='Halloween',
                description=(
                    'Fifteen years after murdering his sister on Halloween '
                    'night 1963, Michael Myers escapes from a mental hospital '
                    'and returns to the small town of Haddonfield, Illinois '
                    'to kill again.'
                )
            )
            db.session.commit()
        headers = get_headers_for_casting_director()

        read_res = self.client().get('/movies', headers=headers)
        self.assertEqual(read_res.status_code, 200)

        post_data = {
            'title': 'Random Movie',
            'description': "This is a random movie that won't get made"
        }
        post_res = self.client().post(
            '/movies',
            json=post_data,
            headers=headers
        )
        self.assertEqual(post_res.status_code, 401)

        patch_data = {
            'title': 'Halloween',
            'description': (
                'This is now a new reboot of the classic horror franchise.'
            )
        }
        patch_res = self.client().patch(
            '/movies/1',
            json=patch_data,
            headers=headers
        )
        self.assertEqual(patch_res.status_code, 200)

        delete_res = self.client().delete('/movies/1', headers=headers)
        self.assertEqual(delete_res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
