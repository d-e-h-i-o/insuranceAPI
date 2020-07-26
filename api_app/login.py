from api_app.validation import LoginError, PayloadError, validate_password
from api_app.validation import String
from unicodedata import normalize
from flask_login import login_user
from api_app.db import db_session
from flask_login import LoginManager
from flask import jsonify


class Login:
    """Logs-in a registered user."""
    username = String(minsize=1, maxsize=64)

    def __init__(self, **kwargs):
        """
        Login object
            1) validates login payload
            2) checks if user exists
            3) checks password
        """

        '1) validate login payload'
        if not kwargs:
            raise PayloadError('''Invalid data. Must be of type "application/json" and contain the following fields:
                                "username": String
                                "password": String
                                ''')
        try:
            self.username = kwargs.get('username')
            validate_password(kwargs.get('password', None))
        except ValueError as e:
            raise PayloadError(str(e))

        self.normalised_username = normalize('NFC', self.username)

        '2) check if user exists and 3) check password'
        self.authenticate(kwargs['password'])

    def authenticate(self, password):
        """Helper functions that queries the database for the user and checks the password."""
        user = db_session.query(User).filter_by(username=self.normalised_username).first()
        if user is None:
            raise LoginError('User is not registered.')
        if not user.check_password(password):
            raise LoginError('Wrong password.')
        login_user(user)


def login_handler(app):
    from api_app.user import User

    login_manager = LoginManager(app)

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({'Error': 'Not authorized. Please log in.'}), 401

    @login_manager.user_loader
    def load_user(id):
        return db_session.query(User).get(int(id))

    return app
