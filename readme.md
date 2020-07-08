<!-- omit in toc -->
# Udacity Casting Agency
<!-- omit in toc -->
## The Capstone project for Udacity Full Stack Nanodegree
This project was created as per the Udacity casting agency rubric.
<!-- omit in toc -->
## Table of Contents
- [1. Getting Started](#1-getting-started)
  - [1.1. Installing Dependencies](#11-installing-dependencies)
    - [1.1.1. Python 3.8](#111-python-38)
    - [1.1.2. Virtual Environment](#112-virtual-environment)
    - [1.1.3. PIP Dependencies](#113-pip-dependencies)
    - [1.1.4. Project Key Dependencies](#114-project-key-dependencies)
- [2. setting up](#2-setting-up)
  - [2.1. setting up the environment variables](#21-setting-up-the-environment-variables)
- [3. using the app](#3-using-the-app)
  - [3.1. Using the app online](#31-using-the-app-online)
  - [3.2. Running the app locally](#32-running-the-app-locally)
- [4. API Reference](#4-api-reference)
  - [4.1. General](#41-general)
    - [4.1.1. Base URL:](#411-base-url)
    - [4.1.2. Authentication:](#412-authentication)
    - [4.1.3. Headers](#413-headers)
  - [4.2. error Handlers](#42-error-handlers)
  - [4.3. Endpoints](#43-endpoints)
    - [4.3.1. GET `/actors`](#431-get-actors)
    - [4.3.2. POST `/actors/<int:id>`](#432-post-actorsintid)
    - [4.3.3. GET `/actors/<int:id>`](#433-get-actorsintid)
    - [4.3.4. PATCH `/actors/<int:id>`](#434-patch-actorsintid)
    - [4.3.5. PATCH `/actors/<int:id>/movies`](#435-patch-actorsintidmovies)
    - [4.3.6. DELETE `/actors/<int:id>/movies`](#436-delete-actorsintidmovies)
    - [4.3.7. DELETE `/actors/<int:id>`](#437-delete-actorsintid)
    - [4.3.8. GET `/movies`](#438-get-movies)
    - [4.3.9. POST `/movies/<int:id>`](#439-post-moviesintid)
    - [4.3.10. GET `/movies/<int:id>`](#4310-get-moviesintid)
    - [4.3.11. PATCH `/movies/<int:id>`](#4311-patch-moviesintid)
    - [4.3.12. PATCH `/movies/<int:id>/actors`](#4312-patch-moviesintidactors)
    - [4.3.13. DELETE `/movies/<int:id>/actors`](#4313-delete-moviesintidactors)
    - [4.3.14. DELETE `/movies/<int:id>`](#4314-delete-moviesintid)
- [5. Testing](#5-testing)

## 1. Getting Started

### 1.1. Installing Dependencies


#### 1.1.1. Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


#### 1.1.2. Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
also, checkout [pipenv](https://pypi.org/project/pipenv/), as it's a great package to manage virtual environments.


#### 1.1.3. PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the root directory and running:

```
bash
pip install -r requirements.txt
```
or
```
bash
pipenv install -r requirements.txt
```

This will install all the required packages we selected within the `requirements.txt` file.


#### 1.1.4. Project Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [Gunicorn](https://gunicorn.org/) as a python wsgi server

## 2. setting up

Follow these setup instructions to get the project up and running

### 2.1. setting up the environment variables
Before running the project, you should set some environment variables, preferably in your ```.env``` file.
the environment variables for the project are found in the [env_example](env_example) file. You can put them in a `.env` file in the root of your virtual environment, or set the variables in the terminal as follows:
```
bash
export FLASK_CONFIG=development
```

## 3. using the app

### 3.1. Using the app online

To use the app online, you can use the created heroku app at [https://a2h-fsnd-capstone.herokuapp.com](https://a2h-fsnd-capstone.herokuapp.com)

### 3.2. Running the app locally
If you want to run the server locally:
From within the root directory, ensure you are working using your created virtual environment.

To run the server, execute:

```
bash
python wsgi.py
```

## 4. API Reference

### 4.1. General

#### 4.1.1. Base URL:

- when using the app hosted on Heroku, the base URL is `https://a2h-fsnd-capstone.herokuapp.com`
- when using the app locally, the app is available under the port 5000. The API base URL is `http://localhost:5000`

#### 4.1.2. Authentication:
This app requires authentication with [auth0](https://auth0.com).
to get the token for the desired user, navigate to `baseurl/`. E.G: [https://a2h-fsnd-capstone.herokuapp.com](https://a2h-fsnd-capstone.herokuapp.com). You'll be redirected to auth0 Login page. After loging in, you'll be redirected back to the application, where you'll find the JWT for the current user. This JWT will be valid for 24 hours for all API requests.
the following users have been created for your convenience:

- Casting Assistant:
  - can get all actors and movies
  - username: `a2h.alshmasi+assistant@gmail.com`
  - password: `Udacity-AssistantPassword`
- Casting Director:
  - can post and delete actors, and patch movies
  - username: `a2h.alshmasi+director@gmail.com`
  - password: `Udacity-DirectorPassword`
- Casting Producer:
  - can post and delete movies
  - username: `a2h.alshmasi+producer@gmail.com`
  - password: `Udacity-ProducerPassword

#### 4.1.3. Headers

You must send the following headers with each request:
- `Content-Type: application/json`
- `Authorization: bearer <jwt>` where jwt is obtained when loging in to the app.

### 4.2. error Handlers

if any errors accured, the API will return a json object in the following format:

```
{
    "success": False,
    "code": 404,
    "message": "not found"
}
```

The following errors will be reported:

- 400: `bad request`
- 404: `resource not found`
- 405: `method not allowed`
- 422: `unprocessible`

### 4.3. Endpoints

#### 4.3.1. GET `/actors`
- Fetches a list that has objects of all actors.
- Request Arguments: None
- Returns: An object with the following keys:
    - `actors`: a list that contains objects of actors.
        - int:`id`: Actor id.
        - str:`name`: actor name.
        - int:`age`: actor age.
        - str:`gender`: actor gender.
        - list:`movies`: a list of movie objects which are assigned to this actor
          - int:`id`: the movie's ID.
          - str:`title`: the movie's title.
          - str:`release_date`: the movie's release date.
- example: `curl https://a2h-fsnd-capstone.herokuapp.com/actors -H "Content-Type: application/json" -H "Authorisation: bearer <jwt>"`

#### 4.3.2. POST `/actors/<int:id>`
- post a new actor.
- Request Arguments:
  - str:`name`: actor name.
  - int:`age`: actor age.
  - str:`gender`: actor gender.
- Returns: An object with the following keys:
    - `actors`: a list that contains an object of the created actor.
        - int:`id`: Actor id.
        - str:`name`: actor name.
        - int:`age`: actor age.
        - str:`gender`: actor gender.
        - list:`movies`: a list of movie objects which are assigned to this actor
          - int:`id`: the movie's ID.
          - str:`title`: the movie's title.
          - str:`release_date`: the movie's release date.
- example: `curl -X 'POST' https://a2h-fsnd-capstone.herokuapp.com/actors -H "Content-Type: application/json" -H "Authorisation: bearer <jwt>" -d '{"name": "Actor 1", "age": "42", "gender": "male"}'`

#### 4.3.3. GET `/actors/<int:id>`
- Fetches the details of the actor with the ID specified in the URL parameters.
- Request Arguments: None
- Returns: An object with the following keys:
    - `actors`: a list that contains an object of the requested actor.
        - int:`id`: Actor id.
        - str:`name`: actor name.
        - int:`age`: actor age.
        - str:`gender`: actor gender.
        - list:`movies`: a list of movie objects which are assigned to this actor
          - int:`id`: the movie's ID.
          - str:`title`: the movie's title.
          - str:`release_date`: the movie's release date.
- example: `curl https://a2h-fsnd-capstone.herokuapp.com/actors/1 -H "Content-Type: application/json" -H "Authorisation: bearer <jwt>"`

#### 4.3.4. PATCH `/actors/<int:id>`
- updates the details of the actor with the ID specified in the URL parameters.
- Request Arguments: one or more of the following Arguments, which will be updated in the database:
  - str:`name`: actor name.
  - int:`age`: actor age.
  - str:`gender`: actor gender.
- Returns: An object with the following keys:
    - `actors`: a list that contains an object of the requested actor.
        - int:`id`: Actor id.
        - str:`name`: actor name.
        - int:`age`: actor age.
        - str:`gender`: actor gender.
        - list:`movies`: a list of movie objects which are assigned to this actor
          - int:`id`: the movie's ID.
          - str:`title`: the movie's title.
          - str:`release_date`: the movie's release date.
- example: `curl -X 'PATCH' https://a2h-fsnd-capstone.herokuapp.com/actors/1 -H "Content-Type: application/json" -H "Authorisation: bearer <jwt>" -d '{"name": "Updated Actor"}'`

#### 4.3.5. PATCH `/actors/<int:id>/movies`
- assigns a movie to the actor with the ID specified in the URL parameters.
- Request Arguments:
  - int:`movie_id`: the movie id which will be assigned to the actor.
- Returns: An object with the following keys:
    - `actors`: a list that contains an object of the requested actor.
        - int:`id`: Actor id.
        - str:`name`: actor name.
        - int:`age`: actor age.
        - str:`gender`: actor gender.
        - list:`movies`: a list of movie objects which are assigned to this actor
          - int:`id`: the movie's ID.
          - str:`title`: the movie's title.
          - str:`release_date`: the movie's release date.
        - str:`gender`: actor gender.
- example: `curl -X 'PATCH' https://a2h-fsnd-capstone.herokuapp.com/actors/1/movies -H "Content-Type: application/json" -H "Authorisation: bearer <jwt>" -d '{"movie_id": "1"}'`

#### 4.3.6. DELETE `/actors/<int:id>/movies`
- unassigns a movie from the actor with the ID specified in the URL parameters.
- Request Arguments:
  - int:`movie_id`: the movie id which will be unassigned from the actor.
- Returns: An object with the following keys:
    - `actors`: a list that contains an object of the requested actor.
        - int:`id`: Actor id.
        - str:`name`: actor name.
        - int:`age`: actor age.
        - str:`gender`: actor gender.
        - list:`movies`: a list of movie objects which are assigned to this actor
          - int:`id`: the movie's ID.
          - str:`title`: the movie's title.
          - str:`release_date`: the movie's release date.
        - str:`gender`: actor gender.
- example: `curl -X 'DELETE' https://a2h-fsnd-capstone.herokuapp.com/actors/1/movies -H "Content-Type: application/json" -H "Authorisation: bearer <jwt>" -d '{"movie_id": "1"}'`

#### 4.3.7. DELETE `/actors/<int:id>`
- Deletes the actor by the id specified in the URL parameters.
- Request Arguments: None
- Returns: A dictionary that contain delete: actor_id key:value pair.
- example: `curl -X DELETE https://a2h-fsnd-capstone.heroku.com/actors/20 -H "Content-Type: application/json" -H "Authorization: bearer <jwt>"`

#### 4.3.8. GET `/movies`
- Fetches a list that has objects of all movies.
- Request Arguments: None
- Returns: An object with the following keys:
    - `movies`: a list that contains objects of movies.
        - int:`id`: Movie id.
        - str:`title`: movie title.
        - str:`release_date`: movie release date.
        - list:`actors`: a list of actor objects which are assigned to this movie
          - int:`id`: the actor's ID.
          - str:`name`: the actor's name.
          - int:`age`: the actor's age.
          - str:`release_date`: the actor's age.
- example: `curl https://a2h-fsnd-capstone.herokuapp.com/movies -H "Content-Type: application/json" -H "Authorisation: bearer <jwt>"`

#### 4.3.9. POST `/movies/<int:id>`
- post a new movie.
- Request Arguments:
  - str:`title`: movie title.
  - str:`release_date`: movie release date.
- Returns: An object with the following keys:
    - `movies`: a list that contains an object of the created movie.
        - int:`id`: Movie id.
        - str:`title`: movie title.
        - str:`release_date`: movie release date.
        - list:`actors`: a list of actor objects which are assigned to this movie
          - int:`id`: the actor's ID.
          - str:`name`: the actor's name.
          - int:`age`: the actor's age.
          - str:`gender`: the actor's gender.
- example: `curl -X 'POST' https://a2h-fsnd-capstone.herokuapp.com/movies -H "Content-Type: application/json" -H "Authorisation: bearer <jwt>" -d '{"title": "The ultimate Trial", "release_date": "01/01/2021"}'`

#### 4.3.10. GET `/movies/<int:id>`
- Fetches the details of the movie with the ID specified in the URL parameters.
- Request Arguments: None
- Returns: An object with the following keys:
    - `movies`: a list that contains an object of the requested movie.
        - int:`id`: Movie id.
        - str:`title`: movie title.
        - str:`release_date`: movie release date.
        - list:`actors`: a list of actor objects which are assigned to this movie
          - int:`id`: the actor's ID.
          - str:`name`: the actor's name.
          - int:`age`: the actor's age.
          - str:`gender`: the actor's gender.
- example: `curl https://a2h-fsnd-capstone.herokuapp.com/movies/1 -H "Content-Type: application/json" -H "Authorisation: bearer <jwt>"`

#### 4.3.11. PATCH `/movies/<int:id>`
- updates the details of the movie with the ID specified in the URL parameters.
- Request Arguments: one or more of the following Arguments, which will be updated in the database:
  - str:`title`: movie title.
  - str:`release_date`: movie release date.
- Returns: An object with the following keys:
    - `movies`: a list that contains an object of the requested movie.
        - int:`id`: Movie id.
        - str:`title`: movie title.
        - str:`release_date`: movie release date.
        - list:`actors`: a list of actor objects which are assigned to this movie
          - int:`id`: the actor's ID.
          - str:`name`: the actor's name.
          - int:`age`: the actor's age.
          - str:`gender`: the actor's gender.
- example: `curl -X 'PATCH' https://a2h-fsnd-capstone.herokuapp.com/movies/1 -H "Content-Type: application/json" -H "Authorisation: bearer <jwt>" -d '{"release_date": "01/01/2022"}'`

#### 4.3.12. PATCH `/movies/<int:id>/actors`
- assigns a actor to the movie with the ID specified in the URL parameters.
- Request Arguments:
  - int:`actor_id`: the actor id which will be assigned to the movie.
- Returns: An object with the following keys:
    - `movies`: a list that contains an object of the requested movie.
        - int:`id`: Movie id.
        - str:`title`: movie title.
        - str:`release_date`: movie release_date.
        - list:`actors`: a list of actor objects which are assigned to this movie
          - int:`id`: the actor's ID.
          - str:`name`: the actor's name.
          - int:`age`: the actor's age.
          - str:`gender`: the actor's gender.
- example: `curl -X 'PATCH' https://a2h-fsnd-capstone.herokuapp.com/movies/1/actors -H "Content-Type: application/json" -H "Authorisation: bearer <jwt>" -d '{"actor_id": "1"}'`

#### 4.3.13. DELETE `/movies/<int:id>/actors`
- unassigns a actor from the movie with the ID specified in the URL parameters.
- Request Arguments:
  - int:`actor_id`: the actor id which will be unassigned from the movie.
- Returns: An object with the following keys:
    - `movies`: a list that contains an object of the requested movie.
        - int:`id`: Movie id.
        - str:`title`: movie title.
        - str:`release_date`: movie release date.
        - list:`actors`: a list of actor objects which are assigned to this movie
          - int:`id`: the actor's ID.
          - str:`name`: the actor's name.
          - int:`age`: the actor's age.
          - str:`gender`: the actor's gender.
- example: `curl -X 'DELETE' https://a2h-fsnd-capstone.herokuapp.com/movies/1/actors -H "Content-Type: application/json" -H "Authorisation: bearer <jwt>" -d '{"actor_id": "1"}'`

#### 4.3.14. DELETE `/movies/<int:id>`
- Deletes the movie by the id specified in the URL parameters.
- Request Arguments: None
- Returns: A dictionary that contain delete: movie_id key:value pair.
- example: `curl -X DELETE https://a2h-fsnd-capstone.heroku.com/movies/20 -H "Content-Type: application/json" -H "Authorization: bearer <jwt>"`

## 5. Testing

The app uses `unittest` for testing all functionalities. Create a testing database and store the URI in the `TEST_DATABASE_URI` environment.
for the tests to run properly, you need to set the `ASSISTANT_TOKEN`, `DIRECTOR_TOKEN`, and `PRODUCER_TOKEN` environment variables with the tokens you get when loging in with the three accounts stated above accordingly.
To run the tests, run
```
bash
python test_app.py
```

