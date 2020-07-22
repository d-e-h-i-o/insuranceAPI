#from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from api_app.validation import RegistrationError, LoginError, Email, PayloadError, validate_password
from api_app.validation import String as StringValidator
from unicodedata import normalize
from flask_login import UserMixin, login_user, current_user
from sqlalchemy import Column, Integer, String
from api_app.db import Base, db_session



class User(UserMixin, Base):
    """Represents a user, includes extensive validation at initialisation."""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(64), index=True, unique=True)
    password_hash = Column(String(128))

    validated_username = StringValidator(minsize=1, maxsize=64)
    validated_email = Email()

    def __init__(self, **kwargs):
        """ Initialises and validates new user.
        Checks if
            1) user is already logged in
            2) parameters are valid
            3) username or email is already in database
        and normalises the username string and sets the password as a hash.

        Database commit and login is only triggered by calling register().
        """

        '1) is user already logged in?'
        #if current_user.is_authenticated:
            #raise RegistrationError("Already authenticated.")

        '2) parameter validation:'
        self.validate_payload(**kwargs)

        'Init:'
        self.username = normalize('NFC', self.validated_username)
        self.email = self.validated_email
        self.set_password(kwargs['password'])

        '3) registration validation:'
        self.validate_registration()

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def validate_payload(self, **kwargs):
        """
        Validates the payload. Not as elegant as in questionnaire, but I do not know how to use both db.Column
        and the validations classes.
        """

        if not kwargs:
            raise PayloadError('''Invalid data. Must be of type application/json and contain the following fields:
                                username: string,
                                email: string,
                                password: string
                                ''')
        try:
            self.validated_username = kwargs.get('username', None)
            self.validated_email = kwargs.get('email', None)
            validate_password(kwargs.get('password', None))
        except ValueError as e:
            raise PayloadError(str(e))
        except Exception as e:
            print(e)
            raise PayloadError('''Invalid registration: Must be of format:
                               "user_name": String,
                               "password": String
                                ''')

    def validate_registration(self):
        """Checks if the username or the email already exists."""
        try:
            session = db_session()
            if session.query(User).filter_by(username=self.username).first() is not None:
                raise RegistrationError("Username is already taken.")
            if session.query(User).filter_by(email=self.email).first() is not None:
                raise RegistrationError("Email is already registered.")
            '''
            if User.query.filter_by(username=self.username).first() is not None:
                raise RegistrationError("Username is already taken.")
            if User.query.filter_by(email=self.email).first() is not None:
                raise RegistrationError("Email is already registered.")
            '''
        except ValueError as e:
            raise RegistrationError(str(e))

    def register(self):
        """Save the user instance in the database and log the user in."""
        db_session.add(self)
        db_session.commit()
        login_user(self)


class Login:
    """Logs-in a registered user."""
    username = StringValidator(minsize=1, maxsize=64)

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
                                "user_name": String
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
