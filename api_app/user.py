from werkzeug.security import generate_password_hash, check_password_hash
from api_app.validation import RegistrationError, Email, PayloadError, validate_password
from api_app.validation import String as StringValidator  # To prevent namespace collision with sqlalchemy String
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

    'Not as elegant as in questionnaire, but I do not know how to use both db.Column and the validations classes.'
    _username = StringValidator(minsize=1, maxsize=64)
    _email = Email()

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
        if current_user.is_authenticated:
            raise RegistrationError("Already authenticated.")

        '2) parameter validation:'
        self.validate_payload(**kwargs)

        'Init:'
        self.username = normalize('NFC', self._username)
        self.email = self._email
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
        Validates the payload.
        """

        if not kwargs:
            raise PayloadError('''Invalid data. Must be of type application/json and contain the following fields:
                                username: string,
                                email: string,
                                password: string
                                ''')
        try:
            self._username = kwargs.get('username', None)
            self._email = kwargs.get('email', None)
            validate_password(kwargs.get('password', None))
        except (ValueError, PayloadError) as e:
            raise PayloadError(str(e))
        except Exception as e:
            print(e)
            raise PayloadError('''Invalid registration: Must be of format:
                               "username": String,
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
        except ValueError as e:
            raise RegistrationError(str(e))

    def register(self):
        """Save the user instance in the database and log the user in."""
        db_session.add(self)
        db_session.commit()
        login_user(self)


