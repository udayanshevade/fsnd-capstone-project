from flask import abort, Blueprint, jsonify, request
from datetime import datetime
from db import db
from models import Actor

actors_blueprint = Blueprint(
  'actors_blueprint',
  __name__,
)

@actors_blueprint.route('/actors', methods=['GET'])
def get_actors():
  """Handles GET requests for all available actors."""
  try:
    print('Request - [GET] /actors')
    actors = Actor.query.all()
    return jsonify({
      'success': True,
      'actors': [actor.format() for actor in actors]
    }), 200
  except Exception as e:
    print('Error - [GET] /actors', e)
    abort(500, 'Internal server error')
  finally:
    db.session.close

@actors_blueprint.route('/actors/<int:actor_id>', methods=['GET'])
def get_actor(actor_id: int):
  """Handles GET requests for a single actor"""
  try:
    print('Request - [GET] /actors/<int:actor_id>')
    actor = Actor.query.get(actor_id)
    return jsonify({
      'success': True,
      'actor': actor.format(),
    }), 200
  except Exception as e:
    print('Error - [GET] /actors/<int:actor_id>', e)
    abort(500, 'Internal server error')
  finally:
    db.session.close()

@actors_blueprint.route('/actors/<int:actor_id>', methods=['PATCH'])
def update_actor(actor_id: int):
  """Handles PATCH requests to update existing actors in the database"""
  try:
    print('Request - [PATCH] /actors/<int:actor_id>')
    actor = Actor.query.get(actor_id)
    if not actor:
      abort(404)
    body = request.get_json()

    if 'name' in body:
      actor.name = body['name']

    if 'birthdate' in body:
      birthdate = body['birthdate']
      try:
        birthdate = datetime.fromisoformat(birthdate)
      except Exception as e:
        print('Error - [PATCH] /actors/<int:actor_id>', e)
        abort(400, 'Invalid birthdate')

      actor.birthdate = body['birthdate']

    # commit changes
    actor.update()

    return jsonify({
      'success': True,
      'actor': actor.format()
    }), 200
  except Exception as e:
    print('Error - [PATCH] /actors/<int:actor_id>', e)
    abort(500, 'Internal server error')
  finally:
    db.session.close()