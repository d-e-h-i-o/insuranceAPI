from flask import Flask
from api_app.db import init_db, init_engine
from api_app.validation import RegistrationError, LoginError, PayloadError
from flask_login import LoginManager
import os


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('../config.py')
        app.config['DATABASE'] = 'postgresql:///insuranceapi_dev'
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    with app.app_context():
        init_engine(app.config['DATABASE'])
        init_db()

    from api_app.db import db_session
    from api_app.routes import register_routes

    app = register_routes(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app

# if __name__ == '__main__':
#    app.run()
