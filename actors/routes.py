from flask import abort, Blueprint, jsonify
from models import db, Actor

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
      'actors': actors
    }), 200
  except Exception as e:
    print('Error - [GET] /actors', e)
    abort(500, 'Internal server error')
  finally:
    db.session.close

@actors_blueprint.route('/actors/<int:actor_id>', methods=['GET'])
def get_actor(payload, actor_id: int):
  try:
    print('Request - [GET] /actors/<int:actor_id>')
    actor = Actor.query.get(actor_id)
    return jsonify({
      'success': True,
      'actor': actor,
    }), 200
  except Exception as e:
    print('Error - [GET] /actors/<int:actor_id>', e)
    abort(500, 'Internal server error')
  finally:
    db.session.close()
