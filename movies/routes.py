from flask import abort, Blueprint, jsonify, request
from db import db
from models import Movie
from auth import requires_auth


movies_blueprint = Blueprint(
    'movies_blueprint',
    __name__,
)


@movies_blueprint.route('/movies', methods=['GET'])
@requires_auth(permission='get:movies')
def get_movies(self):
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
        code = getattr(e, 'code', 500)
        abort(code)
    finally:
        db.session.close()


@movies_blueprint.route('/movies', methods=['POST'])
@requires_auth(permission='post:movies')
def create_movie(self):
    """Handles POST requests to create a new movies"""
    try:
        print('Request - [POST] /movies')
        body = request.get_json()

        required_attrs = ('title', 'description')
        if not all(attr in body for attr in required_attrs):
            abort(400)

        movie = Movie(title=body['title'], description=body['description'])

        # add and commit
        movie.insert()

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
    except Exception as e:
        print('Error - [POST] /movies', e)
        code = getattr(e, 'code', 500)
        abort(code)
    finally:
        db.session.close()


@movies_blueprint.route('/movies/<int:movie_id>', methods=['GET'])
@requires_auth(permission='get:movies')
def get_movie(self, movie_id: int):
    """Handles GET requests for a specified movie."""
    try:
        print('Request - [GET] /movies/<int:movie_id>')
        movie = Movie.query.get(movie_id)

        if not movie:
            abort(404)

        return jsonify({
            'success': True,
            'movie': movie.format(),
        }), 200
    except Exception as e:
        print('Error - [GET] /movies/<int:movie_id>', e)
        code = getattr(e, 'code', 500)
        abort(code)
    finally:
        db.session.close()


@movies_blueprint.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth(permission='patch:movies')
def update_movie(self, movie_id: int):
    """Handles PATCH requests to update existing movies in the database"""
    try:
        print('Request - [PATCH] /movies/<int:movie_id>')
        movie = Movie.query.get(movie_id)

        if not movie:
            abort(404)

        body = request.get_json()

        if 'title' in body:
            movie.title = body['title']

        if 'description' in body:
            movie.description = body['description']

        # commit changes
        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
    except Exception as e:
        print('Error - [PATCH] /movies/<int:movie_id>', e)
        code = getattr(e, 'code', 500)
        abort(code)
    finally:
        db.session.close()


@movies_blueprint.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth(permission='delete:movies')
def delete_movie(self, movie_id: int):
    """Handles DELETE requests to remove existing movies in the database"""
    try:
        print('Request - [PATCH] /movies/<int:movie_id>')

        movie = Movie.query.get(movie_id)

        if not movie:
            abort(404)

        # remove and commit
        movie.delete()

        return jsonify({
            'success': True,
            'removed': movie_id
        })
    except Exception as e:
        print('Error - [PATCH] /movies/<int:movie_id>', e)
        code = getattr(e, 'code', 500)
        abort(code)
    finally:
        db.session.close()
