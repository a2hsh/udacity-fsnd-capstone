# errors.py
from . import main
from ..auth.auth import AuthError
from flask import abort, jsonify
from werkzeug.exceptions import HTTPException
# error handlers

'''
error handler for authorization errors
'''


@main.errorhandler(AuthError)
def authorization_error(error):
    return jsonify({
        'success': False,
        'code': error.status_code,
        'message': error.error
    }), error.status_code


'''
error handler for internal server errors
'''


@main.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'code': 500,
        'message': 'internal server error'
    }), 500

    '''
error handler for all other errors
'''


@main.errorhandler(Exception)
def other_errors_handler(error):
    return jsonify({
        'success': False,
        'code': error.code,
        'message': error.name
    }), error.code
