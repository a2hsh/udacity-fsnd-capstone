# routes Blueprint
from flask import Blueprint, jsonify, request, redirect, render_template
from flask_cors import CORS
from os import environ
# initializing the blueprint
main = Blueprint('main', __name__)
CORS(main, resources={r'*': {'origins': '*'}})


@main.after_request
def after_request(response):
    '''defining extra headers'''
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PATCH,POST,DELETE,OPTIONS')
    response.headers.add('Content-Type', 'application/json')
    return response


# importing routes
from . import actors, movies, errors
