# actors.py
from . import main
from app import db
from app.database.models import Actor, Movie
from flask import abort, request, redirect, jsonify
from sqlalchemy import exc
from ..auth.auth import requires_auth

# handling routes for actors endpoints
'''
endpoint
    GET /actors
        requires the 'get:actor-details' permission
        contains the actor's data representation
    returns status code 200 and json {
        "success": True,
        "actors": [actors]
    } where "actors" is a list with all actors
        or appropriate status code indicating reason for failure
'''


@main.route('/actors')
@requires_auth('get:actor-details')
def get_actors(payload):
    try:
        actors = Actor.query.all()
        if not actors:
            abort(404)
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        })
    except Exception as error:
        raise error


'''
endpoint
    GET /actors/<id>
        requires the 'get:actor-details' permission
        contains the actor's data representation
    returns status code 200 and json {
        "success": True,
        "actors": actor} for a given actor
        or appropriate status code indicating reason for failure
'''


@main.route('/actors/<id>')
@requires_auth('get:actor-details')
def get_actor_details(payload, id):
    try:
        actor = Actor.query.get(id)
        if not actor:
            abort(404)
        return jsonify({
            'success': True,
            'actors': [actor.format()]
        })
    except Exception as error:
        raise error


'''
endpoint
    POST /actors
        creates a new row in the actors table
        requires the 'post:actors' permission
        it should contain the actor data representation
    returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the newly created actor
        or appropriate status code indicating reason for failure
'''


@main.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_actor(payload):
    try:
        # get json from body
        body = request.get_json()
        # Raise a 400 error if the name, age, or gender are not in body
        if 'name' not in body or 'age' not in body or 'gender' not in body:
            abort(400)
        # insure that the name, age, and gender are strings
        if not isinstance(body['name'], str) or not isinstance(body['age'], str) or not isinstance(body['gender'], str):
            abort(400)
        actor = Actor(
            name=body['name'],
            age=body['age'],
            gender=body['gender']
        )
        # insert the new actor to the database
        actor.insert()
        return jsonify({
            'success': True,
            'actors': [actor.format()]
        })
    except exc.SQLAlchemyError:
        abort(422)
    except Exception as error:
        raise error


'''
endpoint
    PATCH /actors/<id>
        where <id> is the existing model id
        responds with a 404 error if <id> is not found
        updates the corresponding row for <id>
        requires the 'patch:actors' permission
        it should contain the actor's json data representation
    returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the updated actor
        or appropriate status code indicating reason for failure
'''


@main.route('/actors/<id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(payload, id):
    try:
        actor = Actor.query.get(id)
        if actor is None:
            abort(404)
        # get json from body
        body = request.get_json()
        # Raise a 400 error if the name, age, and gender are not strings, or empty
        if 'name' not in body and 'age' not in body and 'gender' not in body:
            abort(400)
        # update the age if it's available in the request body
        if 'name' in body:
            if not isinstance(body['name'], str):
                # name is not a string
                abort(400)
            # update the actor's title
            actor.name = body['name']
        # update the age if it's available in the request body
        if 'age' in body:
            # check that the age is a string
            if not isinstance(body['age'], str):
                # age is not a string
                abort(400)
            # update the actor's age
            actor.age = body['age']
        # update the gender if it's available in the request body
        if 'gender' in body:
            # check that the gender is a string
            if not isinstance(body['gender'], str):
                # gender is not a string
                abort(400)
            # update the actor's gender
            actor.gender = body['gender']
        # update the actor in the database
        actor.update()
        return jsonify({
            'success': True,
            'actors': [actor.format()]
        })
    except exc.SQLAlchemyError:
        abort(422)
    except Exception as error:
        raise error


'''
endpoint
    DELETE /actors/<id>
        where <id> is the existing model id
        responds with a 404 error if <id> is not found
        deletes the corresponding row for <id>
        requires the 'delete:actors' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@main.route('/actors/<id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, id):
    try:
        actor = Actor.query.get(id)
        # returns a 404 error if the actor is not found
        if actor is None:
            abort(404)
        # delete the actor
        actor.delete()
        return jsonify({
            'success': True,
            'delete': id
        })
    except exc.SQLAlchemyError:
        abort(422)
    except Exception as error:
        raise error


'''
endpoint
    POST /actors/<id>
        where <id> is the existing actor id
        responds with a 404 error if <id> is not found
        adds a movie to the corresponding actor data for <id>
        requires the 'patch:actors' permission
        it should contain the actor's json data representation
    returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the updated actor
        or appropriate status code indicating reason for failure
'''


@main.route('/actors/<id>/movies', methods=['POST'])
@requires_auth('patch:actors')
def add_movie_to_actor(payload, id):
    try:
        actor = Actor.query.get(id)
        if actor is None:
            abort(404)
        # get json from body
        body = request.get_json()
        # Raise a 400 error if the movie_id is empty
        if 'movie_id' not in body or not isinstance(body['movie_id'], str):
            # either the movie_id is not in the body or it's not a string
            abort(400)
        # add the movie to the actor if the movie is available in the database
        movie = Movie.query.get(body['movie_id'])
        if movie is None:
            # trying to append a movie with an envalid movie_id should return a 404 error
            abort(404)
        # append the movie to the actor
        actor.movies.append(movie)
        # update the actor in the database
        actor.update()
        return jsonify({
            'success': True,
            'actors': [actor.format()]
        })
    except exc.SQLAlchemyError:
        abort(422)
    except Exception as error:
        raise error


'''
endpoint
    DELETE /actors/<id>
        where <id> is the existing actor id
        responds with a 404 error if <id> is not found
        deletes a movie from the corresponding actor data for <id>
        requires the 'patch:actors' permission
        it should contain the actor's json data representation
    returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the updated actor
        or appropriate status code indicating reason for failure
'''


@main.route('/actors/<id>/movies', methods=['DELETE'])
@requires_auth('patch:actors')
def delete_movie_from_actor(payload, id):
    try:
        actor = Actor.query.get(id)
        if actor is None:
            abort(404)
        # get json from body
        body = request.get_json()
        # Raise a 400 error if the movie_id is empty
        if 'movie_id' not in body or not isinstance(body['movie_id'], str):
            # either the movie_id is not in the body or it's not a string
            abort(400)
        # add the movie to the actor if the movie is available in the database
        movie = Movie.query.get(body['movie_id'])
        if movie is None:
            # trying to delete a movie with an envalid movie_id should return a 404 error
            abort(404)
        # delete the movie from the actor
        actor.movies.remove(movie)
        # update the actor in the database
        actor.update()
        return jsonify({
            'success': True,
            'actors': [actor.format()]
        })
    except exc.SQLAlchemyError:
        abort(422)
    except Exception as error:
        raise error
