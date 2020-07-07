import os
from flask import Flask, jsonify, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import environ

# Instantiating global objects and variables
db = SQLAlchemy()
migrate = Migrate()


def create_app(config=environ.get('FLASK_CONFIG') or 'development'):
    # create and configure the app
    app = Flask(__name__)
    if config == 'development':
        app.config.from_object('config.DevConfig')
    elif config == 'production':
        app.config.from_object('config.ProdConfig')
    elif config == 'testing':
        app.config.from_object('config.TestConfig')
    else:
        raise EnvironmentError(
            'Please specify a valid configuration profile in your FLASK_CONFIG environment variable for the application. Possible choices are `development`, `testing`, or `production`')
    # initializing application extentions
    db.init_app(app)
    migrate.init_app(app, db)
    # bind all extentions to the app instance
    with app.app_context():
        # importing routes blueprint
        from .main import main
        # register blueprints
        app.register_blueprint(main)
        # Public ROUTES
        '''
        endpoint
        GET /
            a public endpoint
            use this endpoint from a browser to login to your account and get an access token for the API
        '''

        @app.route('/')
        def redirect_to_login():
            # redirect to Auth0 login page
            return redirect(f'https://{environ.get("AUTH0_DOMAIN")}/authorize?audience={environ.get("AUTH0_AUDIENCE")}&response_type=token&client_id={environ.get("AUTH0_CLIENT_ID")}&redirect_uri={environ.get("AUTH0_REDIRECT_URI")}')

        @app.route('/token', methods=['GET'])
        def parce_token():
            if 'access_token' in request.args:
                return request.args.get('access_token')
            else:
                return render_template('token.html')

    return app
