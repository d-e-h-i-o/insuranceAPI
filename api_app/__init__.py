""" The app factory function for the Flask app.
The app is structured in 3 abstraction layers:
1) The route layer (route.py) is handles routing and structures the high-level application logic.
2) The endpoint classes (user.py, login.py, questionnaire.py) is where the specific application logic lives.
3) The validation classes (validation.py) is where the payload is validated.

The payload is generally handed downwards the layers, and errors are handed upwards as
custom exceptions, and returned as json.
"""
import os
from flask import Flask
from api_app.db import init_db, init_engine, db_session
from api_app.validation import RegistrationError, LoginError, PayloadError


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY=os.environ['SECRET_KEY'])

    if test_config is None:
        app.config.from_pyfile('../config.py')
        app.config['DATABASE'] = os.environ['DATABASE_URL']
    else:
        app.config.from_mapping(test_config)

    with app.app_context():
        init_engine(app.config['DATABASE'])
        init_db(app)

    from api_app.db import db_session
    from api_app.routes import register_routes
    from api_app.login import login_handler

    app = register_routes(app)
    app = login_handler(app)

    return app


