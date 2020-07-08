# tests for the API
import json
from app import create_app, db
from app.database.models import Actor, Movie
from os import environ
# generating random queries for the data
from sqlalchemy import func, desc
import unittest

# defining variables
if environ.get('ASSISTANT_TOKEN') is None:
    raise EnvironmentError('ASSISTANT_TOKEN is missing')
elif environ.get('DIRECTOR_TOKEN') is None:
    raise EnvironmentError('DIRECTOR_TOKEN is missing')
elif environ.get('PRODUCER_TOKEN') is None:
    raise EnvironmentError('DIRECTOR_TOKEN is missing')
assistant_headers = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer ' + environ.get('ASSISTANT_TOKEN')
}
director_headers = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer ' + environ.get('DIRECTOR_TOKEN')
}
producer_headers = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer ' + environ.get('PRODUCER_TOKEN')
}


class AgencyAPI(unittest.TestCase):
    '''
    base class for testing the API
    '''

    # Setup and teardown methods
    def setUp(self):
        # executed before and after each test.
        # creating the application
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        # push the application context with all extentions
        self.app_context.push()
        with self.app.test_client():
            self.client = self.app.test_client()
            db.drop_all()
            db.create_all()
            actor1 = Actor(
                name='Actor 1',
                age='42',
                gender='male'
            )
            actor2 = Actor(
                name='Actor 2',
                age='33',
                gender='female'
            )
            movie1 = Movie(
                title='The Testing Test',
                release_date='01/01/2021'
            )
            movie2 = Movie(
                title='The Testing Test - sequal',
                release_date='01/01/2023'
            )
            actor1.insert()
            actor2.insert()
            movie1.insert()
            movie2.insert()

    def tearDown(self):
        # pop the app context
        self.app_context.pop()

    def test_get_all_actors(self):
        '''
        tests getting all actors
        '''
        # get response json, then load the data
        response = self.client.get(
            '/actors', headers=assistant_headers)
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # actors should be present in data
        self.assertIn('actors', data)
        # actors length should be more than 0
        self.assertGreater(len(data['actors']), 0)

    def test_missing_auth_actors(self):
        '''test getting all actors without authorisation'''
        # get response json, then load the data
        response = self.client.get(
            '/actors')
        data = json.loads(response.data)
        # status code should be 401
        self.assertEqual(response.status_code, 401)
        # success should be false
        self.assertFalse(data['success'])

    def test_get_actor_details(self):
        # load a random actor from db
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically, then load the data
        response = self.client.get(
            f'/actors/{actor.id}', headers=assistant_headers)
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # actors should be present in data
        self.assertIn('actors', data)
        # actors length should be more than 0
        self.assertGreater(len(data['actors']), 0)

    def test_get_envalid_actor(self):
        '''
        tests getting actors by envalid id
        '''
        # get the last actor from db
        actor = Actor.query.order_by(desc(Actor.id)).first()
        # get response json, then load the data
        response = self.client.get(
            f'/actors/{actor.id + 1}', headers=assistant_headers)
        data = json.loads(response.data)
        # status code should be 404
        self.assertEqual(response.status_code, 404)
        # success should be false
        self.assertFalse(data['success'])

    def test_get_missing_auth_actor(self):
        '''
        tests getting an actor with missing auth headers
        '''
        # load a random actor from db
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically, then load the data
        response = self.client.get(
            f'/actors/{actor.id}')
        data = json.loads(response.data)
        # status code should be 401
        self.assertEqual(response.status_code, 401)
        # success should be false
        self.assertFalse(data['success'])

    def test_empty_post_actor(self):
        '''
        tests posting an empty actor json
        '''
        # get response json, then load the data
        response = self.client.post('/actors',
                                    headers=director_headers,
                                    json={})
        data = json.loads(response.data)
        # status code should be 400
        self.assertEqual(response.status_code, 400)
        # success should be false
        self.assertFalse(data['success'])

    def test_unauthorised_post_actor(self):
        '''
        tests posting new actor with a role below the minimum role
        '''
        # get response json, then load the data
        response = self.client.post('/actors',
                                    headers=assistant_headers,
                                    json={
                                        'name': 'test artist',
                                        'age': '42',
                                        'gender': 'male'
                                    })
        data = json.loads(response.data)
        # status code should be 403
        self.assertEqual(response.status_code, 403)
        # success should be false
        self.assertFalse(data['success'])

    def test_post_actor(self):
        '''
        tests posting a new actor
        '''
        # get response json, then load the data
        response = self.client.post('/actors',
                                    headers=director_headers,
                                    json={
                                        'name': 'test artist',
                                        'age': '42',
                                        'gender': 'male'
                                    })
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # actors should be present in data
        self.assertIn('actors', data)
        # actors length should be more than 0
        self.assertGreater(len(data['actors']), 0)

    def test_empty_patch_actor(self):
        '''
        tests patching an actor with empty json
        '''
        # load a random actor from db
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically, then load the data
        response = self.client.patch(
            f'/actors/{actor.id}', headers=director_headers, json={})
        data = json.loads(response.data)
        # status code should be 400
        self.assertEqual(response.status_code, 400)
        # success should be false
        self.assertFalse(data['success'])

    def test_unauthorised_patch_actor(self):
        '''
        tests patching new actor with a role below the minimum role
        '''
        # load a random actor from db
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically, then load the data
        response = self.client.patch(
            f'/actors/{actor.id}', headers=assistant_headers, json={
                'name': 'updated actor'
            })
        data = json.loads(response.data)
        # status code should be 403
        self.assertEqual(response.status_code, 403)
        # success should be false
        self.assertFalse(data['success'])

    def test_patch_actor(self):
        '''
        tests patching an actor
        '''
        # load a random actor from db
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically, then load the data
        response = self.client.patch(
            f'/actors/{actor.id}', headers=director_headers, json={
                'name': 'updated actor'
            })
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # actors should be present in data
        self.assertIn('actors', data)
        # actors length should be more than 0
        self.assertGreater(len(data['actors']), 0)

    def test_empty_assign_actor_movie(self):
        '''
        tests assigning a movie to an actor with empty json
        '''
        # load a random actor from db
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically, then load the data
        response = self.client.patch(
            f'/actors/{actor.id}/movies', headers=director_headers, json={})
        data = json.loads(response.data)
        # status code should be 400
        self.assertEqual(response.status_code, 400)
        # success should be false
        self.assertFalse(data['success'])

    def test_unauthorised_assign_actor_movie(self):
        '''
        tests assigning a movie to an actor with a role below the minimum role
        '''
        # load  a random actor and movie from db
        actor = Actor.query.order_by(func.random()).first()
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically, then load the data
        response = self.client.patch(
            f'/actors/{actor.id}/movies', headers=assistant_headers, json={
                'movie_id': str(movie.id)
            })
        data = json.loads(response.data)
        # status code should be 403
        self.assertEqual(response.status_code, 403)
        # success should be false
        self.assertFalse(data['success'])

    def test_envalid_assign_actor_movie(self):
        '''
        tests assigning an envalid movie to an actor
        '''
        # get the last actor and movie from db
        actor = Actor.query.order_by(desc(Actor.id)).first()
        movie = Movie.query.order_by(desc(Movie.id)).first()
        movie_id = movie.id
        # get response json, requesting the actor dynamically, then load the data
        response = self.client.patch(
            f'/actors/{actor.id}/movies', headers=director_headers, json={
                'movie_id': str(movie.id + 1)
            })
        data = json.loads(response.data)
        # status code should be 404
        self.assertEqual(response.status_code, 404)
        # success should be false
        self.assertFalse(data['success'])

    def test_assign_actor_movie(self):
        '''
        tests assigning a movie to an actor
        '''
        # load a random actor and a movie from db
        actor = Actor.query.order_by(func.random()).first()
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically, then load the data
        response = self.client.patch(
            f'/actors/{actor.id}/movies', headers=director_headers, json={
                'movie_id': str(movie.id)
            })
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # actors should be present in data
        self.assertIn('actors', data)
        # actors length should be more than 0
        self.assertGreater(len(data['actors']), 0)

    def test_unauthorised_delete_actor(self):
        '''
        tests deleting an actor with a role below the minimum role
        '''
        # load a random actor from db
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically, then load the data
        response = self.client.delete(
            f'/actors/{actor.id}', headers=assistant_headers)
        data = json.loads(response.data)
        # status code should be 403
        self.assertEqual(response.status_code, 403)
        # success should be false
        self.assertFalse(data['success'])

    def test_delete_actor(self):
        '''
        tests deleting an actor
        '''
        # load a random actor from db
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the actor dynamically, then load the data
        response = self.client.delete(
            f'/actors/{actor.id}', headers=director_headers)
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        print(data)
        # delete should be present in data
        self.assertIn('delete', data)

    def test_get_all_movies(self):
        '''
        tests getting all movies
        '''
        # get response json, then load the data
        response = self.client.get(
            '/movies', headers=assistant_headers)
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # movies should be present in data
        self.assertIn('movies', data)
        # movies length should be more than 0
        self.assertGreater(len(data['movies']), 0)

    def test_missing_auth_movies(self):
        '''
        test getting all movies without authorisation
        '''
        # get response json, then load the data
        response = self.client.get(
            '/movies')
        data = json.loads(response.data)
        # status code should be 401
        self.assertEqual(response.status_code, 401)
        # success should be false
        self.assertFalse(data['success'])

    def test_get_movie_details(self):
        # load a random movie from db
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically, then load the data
        response = self.client.get(
            f'/movies/{movie.id}', headers=assistant_headers)
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # movies should be present in data
        self.assertIn('movies', data)
        # movies length should be more than 0
        self.assertGreater(len(data['movies']), 0)

    def test_get_envalid_movie(self):
        '''
        tests getting movies by envalid id
        '''
        # get the last movie from db
        movie = Movie.query.order_by(desc(Movie.id)).first()
        # get response json, then load the data
        response = self.client.get(
            f'/movies/{movie.id + 1}', headers=assistant_headers)
        data = json.loads(response.data)
        # status code should be 404
        self.assertEqual(response.status_code, 404)
        # success should be false
        self.assertFalse(data['success'])

    def test_get_missing_auth_movie(self):
        '''
        tests getting a movie with missing auth headers
        '''
        # load a random movie from db
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically, then load the data
        response = self.client.get(
            f'/movies/{movie.id}')
        data = json.loads(response.data)
        # status code should be 401
        self.assertEqual(response.status_code, 401)
        # success should be false
        self.assertFalse(data['success'])

    def test_empty_post_movie(self):
        '''
        tests posting an empty movie json
        '''
        # get response json, then load the data
        response = self.client.post('/movies',
                                    headers=producer_headers,
                                    json={})
        data = json.loads(response.data)
        # status code should be 400
        self.assertEqual(response.status_code, 400)
        # success should be false
        self.assertFalse(data['success'])

    def test_unauthorised_post_movie(self):
        '''
        tests posting new movie with a role below the minimum role
        '''
        # get response json, then load the data
        response = self.client.post('/movies',
                                    headers=director_headers,
                                    json={
                                        'title': 'test movie',
                                        'release_date': '01/01/2022'
                                    })
        data = json.loads(response.data)
        # status code should be 403
        self.assertEqual(response.status_code, 403)
        # success should be false
        self.assertFalse(data['success'])

    def test_post_movie(self):
        '''
        tests posting a new movie
        '''
        # get response json, then load the data
        response = self.client.post('/movies',
                                    headers=producer_headers,
                                    json={
                                        'title': 'test movie',
                                        'release_date': '01/01/2020',
                                        'gender': 'male'
                                    })
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # movies should be present in data
        self.assertIn('movies', data)
        # movies length should be more than 0
        self.assertGreater(len(data['movies']), 0)

    def test_empty_patch_movie(self):
        '''
        tests patching a movie with empty json
        '''
        # load a random movie from db
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically, then load the data
        response = self.client.patch(
            f'/movies/{movie.id}', headers=director_headers, json={})
        data = json.loads(response.data)
        # status code should be 400
        self.assertEqual(response.status_code, 400)
        # success should be false
        self.assertFalse(data['success'])

    def test_unauthorised_patch_movie(self):
        '''
        tests patching new movie with a role below the minimum role
        '''
        # load a random movie from db
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically, then load the data
        response = self.client.patch(
            f'/movies/{movie.id}', headers=assistant_headers, json={
                'title': 'updated movie'
            })
        data = json.loads(response.data)
        # status code should be 403
        self.assertEqual(response.status_code, 403)
        # success should be false
        self.assertFalse(data['success'])

    def test_patch_movie(self):
        '''
        tests patching a movie
        '''
        # load a random movie from db
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically, then load the data
        response = self.client.patch(
            f'/movies/{movie.id}', headers=director_headers, json={
                'title': 'updated movie'
            })
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # movies should be present in data
        self.assertIn('movies', data)
        # movies length should be more than 0
        self.assertGreater(len(data['movies']), 0)

    def test_empty_assign_movie_actor(self):
        '''
        tests assigning an actor to a movie with empty json
        '''
        # load a random movie from db
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically, then load the data
        response = self.client.patch(
            f'/movies/{movie.id}/actors', headers=director_headers, json={})
        data = json.loads(response.data)
        # status code should be 400
        self.assertEqual(response.status_code, 400)
        # success should be false
        self.assertFalse(data['success'])

    def test_unauthorised_assign_movie_actor(self):
        '''
        tests assigning an actor to a movie with a role below the minimum role
        '''
        # load  a random movie and actor from db
        movie = Movie.query.order_by(func.random()).first()
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically, then load the data
        response = self.client.patch(
            f'/movies/{movie.id}/actors', headers=assistant_headers, json={
                'actor_id': str(actor.id)
            })
        data = json.loads(response.data)
        # status code should be 403
        self.assertEqual(response.status_code, 403)
        # success should be false
        self.assertFalse(data['success'])

    def test_envalid_assign_movie_actor(self):
        '''
        tests assigning an envalid actor to a movie
        '''
        # get the last movie and actor from db
        movie = Movie.query.order_by(desc(Movie.id)).first()
        actor = Actor.query.order_by(desc(Actor.id)).first()
        # get response json, requesting the movie dynamically, then load the data
        response = self.client.patch(
            f'/movies/{movie.id}/actors', headers=director_headers, json={
                'actor_id': str(actor.id + 1)
            })
        data = json.loads(response.data)
        # status code should be 404
        self.assertEqual(response.status_code, 404)
        # success should be false
        self.assertFalse(data['success'])

    def test_assign_movie_actor(self):
        '''
        tests assigning an actor to a movie
        '''
        # load a random movie and an actor from db
        movie = Movie.query.order_by(func.random()).first()
        actor = Actor.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically, then load the data
        response = self.client.patch(
            f'/movies/{movie.id}/actors', headers=director_headers, json={
                'actor_id': str(actor.id)
            })
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        # movies should be present in data
        self.assertIn('movies', data)
        # movies length should be more than 0
        self.assertGreater(len(data['movies']), 0)

    def test_unauthorised_delete_movie(self):
        '''
        tests deleting a movie with a role below the minimum role
        '''
        # load a random movie from db
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically, then load the data
        response = self.client.delete(
            f'/movies/{movie.id}', headers=director_headers)
        data = json.loads(response.data)
        # status code should be 403
        self.assertEqual(response.status_code, 403)
        # success should be false
        self.assertFalse(data['success'])

    def test_delete_movie(self):
        '''
        tests deleting a movie
        '''
        # load a random movie from db
        movie = Movie.query.order_by(func.random()).first()
        # get response json, requesting the movie dynamically, then load the data
        response = self.client.delete(
            f'/movies/{movie.id}', headers=producer_headers)
        data = json.loads(response.data)
        # status code should be 200
        self.assertEqual(response.status_code, 200)
        # success should be true
        self.assertTrue(data['success'])
        print(data)
        # delete should be present in data
        self.assertIn('delete', data)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
