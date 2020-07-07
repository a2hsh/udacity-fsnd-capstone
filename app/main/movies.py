# movies.py
# handling routes for movies endpoints
from . import main
from app import db
from app.database.models import Actor, Movie
from flask import abort, request, redirect, jsonify
from sqlalchemy import exc
from ..auth.auth import requires_auth


'''
endpoint
    GET /movies
        requires the 'get:movie-details' permission
        contains the movie's data representation
    returns status code 200 and json {
        "success": True,
        "movies": [movies]
    } where "movies" is a list with all movies
        or appropriate status code indicating reason for failure
'''


@main.route('/movies/')
@requires_auth('get:movie-details')
def get_movies(payload):
    try:
        movies = Movie.query.all()
        if not movies:
            abort(404)
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        })
    except Exception as error:
        raise error


'''
endpoint
    GET /movies/<id>
        requires the 'get:movie-details' permission
        contains the movie's data representation
    returns status code 200 and json {
        "success": True,
        "movies": [movie] for a given movie
        or appropriate status code indicating reason for failure
'''


@main.route('/movies/<id>')
@requires_auth('get:movie-details')
def get_movie_details(payload, id):
    try:
        movie = Movie.query.get(id)
        if not movie:
            abort(404)
        return jsonify({
            'success': True,
            'movies': [movie.format()]
        })
    except Exception as error:
        raise error


'''
endpoint
    POST /movies
        creates a new row in the movies table
        requires the 'post:movies' permission
        it should contain the movie data representation
    returns status code 200 and json {"success": True, "movies": movie} where movies is an array containing only the newly created movie
        or appropriate status code indicating reason for failure
'''


@main.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movie(payload):
    try:
        # get json from body
        body = request.get_json()
        # Raise a 400 error if the name, age, or gender are not in body
        if 'title' not in body or 'release_date' not in body:
            abort(400)
        # insure that the title and release_date are strings
        if not isinstance(body['title'], str) or not isinstance(body['release_date'], str):
            abort(400)
        movie = Movie(
            title=body['title'],
            release_date=body['release_date']
        )
        # insert the new movie to the database
        movie.insert()
        return jsonify({
            'success': True,
            'movies': [movie.format()]
        })
    except exc.SQLAlchemyError:
        abort(422)
    except Exception as error:
        raise error


'''
endpoint
    PATCH /movies/<id>
        where <id> is the existing model id
        responds with a 404 error if <id> is not found
        updates the corresponding row for <id>
        requires the 'patch:movies' permission
        it should contain the movie's json data representation
    returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the updated movie
        or appropriate status code indicating reason for failure
'''


@main.route('/movies/<id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(payload, id):
    try:
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)
        # get json from body
        body = request.get_json()
        # Raise a 400 error if the title or release_date are not strings, or empty
        if 'title' not in body and 'release_date' not in body:
            abort(400)
        # update the title if it's available in the request body
        if 'title' in body:
            if not isinstance(body['title'], str):
                # title is not a string
                abort(400)
            # update the movie's title
            movie.title = body['title']
        # update the release_date if it's available in the request body
        if 'release_date' in body:
            # check that the title is a string
            if not isinstance(body['release_date'], str):
                # release_date is not a string
                abort(400)
            # update the movie's release_date
            movie.release_date = body['release_date']
        # update the movie in the database
        movie.update()
        return jsonify({
            'success': True,
            'movies': [movie.format()]
        })
    except exc.SQLAlchemyError:
        abort(422)
    except Exception as error:
        raise error


'''
endpoint
    DELETE /movies/<id>
        where <id> is the existing model id
        responds with a 404 error if <id> is not found
        deletes the corresponding row for <id>
        requires the 'delete:movies' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@main.route('/movies/<id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, id):
    try:
        movie = Movie.query.get(id)
        # returns a 404 error if the movie is not found
        if movie is None:
            abort(404)
        # delete the movie
        movie.delete()
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
    POST /movies/<id>
        where <id> is the existing movie id
        responds with a 404 error if <id> is not found
        deletes an actor from the corresponding movie data for <id>
        requires the 'patch:actors' permission
        it should contain the movie's json data representation
    returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the updated movie
        or appropriate status code indicating reason for failure
'''


@main.route('/movies/<id>/actors', methods=['POST'])
@requires_auth('patch:actors')
def add_actor_to_movie(payload, id):
    try:
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)
        # get json from body
        body = request.get_json()
        # Raise a 400 error if the actor_id is empty
        if 'actor_id' not in body or not isinstance(body['actor_id'], str):
            # either the actor_id is not in the body or it's not a string
            abort(400)
        # add the actor to the movie if the actor is available in the database
        actor = Actor.query.get(body['actor_id'])
        if actor is None:
            # trying to append an actor with an envalid actor_id should return a 404 error
            abort(404)
        # append the actor to the movie
        movie.actors.append(actor)
        # update the movie in the database
        movie.update()
        return jsonify({
            'success': True,
            'movies': [movie.format()]
        })
    except exc.SQLAlchemyError:
        abort(422)
    except Exception as error:
        raise error


'''
endpoint
    POST /movies/<id>
        where <id> is the existing movie id
        responds with a 404 error if <id> is not found
        deletes an actor from the corresponding movie data for <id>
        requires the 'patch:movies' permission
        it should contain the movie's json data representation
    returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the updated movie
        or appropriate status code indicating reason for failure
'''


@main.route('/movies/<id>/actors', methods=['DELETE'])
@requires_auth('patch:movies')
def delete_actor_to_movie(payload, id):
    try:
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)
        # get json from body
        body = request.get_json()
        # Raise a 400 error if the actor_id is empty
        if 'actor_id' not in body or not isinstance(body['actor_id'], str):
            # either the actor_id is not in the body or it's not a string
            abort(400)
        # add the actor to the movie if the actor is available in the database
        actor = Actor.query.get(body['actor_id'])
        if actor is None:
            # trying to delete an actor with an envalid actor_id should return a 404 error
            abort(404)
        # delete the actor from the movie
        movie.actors.remove(actor)
        # update the movie in the database
        movie.update()
        return jsonify({
            'success': True,
            'movies': [movie.format()]
        })
    except exc.SQLAlchemyError:
        abort(422)
    except Exception as error:
        raise error
