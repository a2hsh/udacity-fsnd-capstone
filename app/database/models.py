# models.py
# This file contains all models of the database, and their helper functions
from app import db

'''
Actors
Should have unique names
should have age and gender
'''


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    movies = db.relationship('Movie', secondary='actor_movies', backref='actors',
                             lazy=True)

    '''
    insert()
        inserts a new model into the database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            actor = Actor(name=req_name, age=req_age, gender=req_gender)
            actor.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a model from the database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a model in the database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.name = 'Tom Cruise'
            actor.update()
    '''

    def update(self):
        db.session.commit()

    '''
    format()
        returns a json representation of the actor model
    '''

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [{'id': movie.id, 'title': movie.title} for movie in self.movies]
        }


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    release_date = db.Column(db.String(50), nullable=False)

    '''
    insert()
        inserts a new model into the database
        the model must have a unique title
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title)
            movie.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a model from the database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a model in the database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'Sully'
            movie.update()
    '''

    def update(self):
        db.session.commit()

    '''
    format()
        returns a json representation of the movie model
    '''

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [{'id': actor.id, 'name': actor.name} for actor in self.actors]
        }


class ActorMovies(db.Model):
    __tablename__ = 'actor_movies'
    actor_id = db.Column(db.Integer, db.ForeignKey(
        'actors.id', ondelete='CASCADE'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movies.id', ondelete='CASCADE'), primary_key=True)
