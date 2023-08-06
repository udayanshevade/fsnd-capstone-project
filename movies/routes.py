from flask import abort, Blueprint, jsonify
from models import db, Movie


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
      'movies': movies
    }), 200
  except Exception as e:
    print('Error - [GET] /movies', e)
    abort(500, 'Internal server error')
  finally:
    db.session.close
