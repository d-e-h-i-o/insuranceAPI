from flask import Flask, jsonify
from api_app.db import init_db, init_engine, db_session
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
        app.config.from_pyfile('../config.py')
        app.config['DATABASE'] = os.environ['DATABASE_URL']
    else:
        app.config.from_mapping(test_config)

    with app.app_context():
        init_engine(app.config['DATABASE'])
        init_db()

    from api_app.db import db_session
    from api_app.routes import register_routes

    app = register_routes(app)
    app = login_handler(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app


def login_handler(app):

    from api_app.models import User

    login_manager = LoginManager(app)

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({'Error': 'Not authorized. Please log in.'}), 401

    @login_manager.user_loader
    def load_user(id):
        return db_session.query(User).get(int(id))

    return app
