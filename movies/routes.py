from flask import abort, Blueprint, jsonify
from db import db
from models import Movie

movies_blueprint = Blueprint(
  'movies_blueprint',
  __name__,
)

@movies_blueprint.route('/movies', methods=['GET'])
def get_movies():
  """Handles GET requests for all available movies."""
  try:
    print('Request - [GET] /movies')
    movies = Movie.query.all()
    return jsonify({
      'success': True,
      'movies': [movie.format() for movie in movies]
    }), 200
  except Exception as e:
    print('Error - [GET] /movies', e)
    abort(500, 'Internal server error')
  finally:
    db.session.close()

@movies_blueprint.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id: int):
  try:
    print('Request - [GET] /movies/<int:movie_id>')
    movie = Movie.query.get(movie_id)
    return jsonify({
      'success': True,
      'movie': movie.format(),
    }), 200
  except Exception as e:
    print('Error - [GET] /movies/<int:movie_id>', e)
    abort(500, 'Internal server error')
  finally:
    db.session.close()
