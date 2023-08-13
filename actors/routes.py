from flask import abort, Blueprint, jsonify, request
from datetime import datetime
from db import db
from models import Actor
from auth import requires_auth


actors_blueprint = Blueprint(
    'actors_blueprint',
    __name__,
)


@actors_blueprint.route('/actors', methods=['GET'])
@requires_auth(permission='get:actors')
def get_actors(self):
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
        code = getattr(e, 'code', 500)
        abort(code)
    finally:
        db.session.close


@actors_blueprint.route('/actors', methods=['POST'])
@requires_auth(permission='post:actors')
def create_actor(self):
    """Handles POST requests to create a new actor"""
    try:
        print('Request - [POST] /actors')
        body = request.get_json()

        required_attrs = ('name', 'birthdate')
        if not all(attr in body for attr in required_attrs):
            abort(400)

        actor = Actor(name=body['name'], birthdate=body['birthdate'])

        # add and commit
        actor.insert()

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200
    except Exception as e:
        print('Error - [POST] /actors', e)
        code = getattr(e, 'code', 500)
        abort(code)
    finally:
        db.session.close()


@actors_blueprint.route('/actors/<int:actor_id>', methods=['GET'])
@requires_auth(permission='get:actors')
def get_actor(self, actor_id: int):
    """Handles GET requests for a single actor"""
    try:
        print('Request - [GET] /actors/<int:actor_id>')
        actor = Actor.query.get(actor_id)

        if not actor:
            abort(404)

        return jsonify({
            'success': True,
            'actor': actor.format(),
        }), 200
    except Exception as e:
        print('Error - [GET] /actors/<int:actor_id>', e)
        code = getattr(e, 'code', 500)
        abort(code)
    finally:
        db.session.close()


@actors_blueprint.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth(permission='patch:actors')
def update_actor(self, actor_id: int):
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
                abort(422, 'Invalid birthdate')

        actor.birthdate = body['birthdate']

        # commit changes
        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200
    except Exception as e:
        print('Error - [PATCH] /actors/<int:actor_id>', e)
        code = getattr(e, 'code', 500)
        abort(code)
    finally:
        db.session.close()


@actors_blueprint.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth(permission='delete:actors')
def delete_actor(self, actor_id: int):
    """Handles DELETE requests to remove existing actors in the database"""
    try:
        print('Request - [PATCH] /actors/<int:actor_id>')

        actor = Actor.query.get(actor_id)

        if not actor:
            abort(404)

        # remove and commit
        actor.delete()

        return jsonify({
            'success': True,
            'removed': actor_id
        })
    except Exception as e:
        print('Error - [PATCH] /actors/<int:actor_id>', e)
        code = getattr(e, 'code', 500)
        abort(code)
    finally:
        db.session.close()
