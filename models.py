from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from validation import String, RegistrationError, LoginError, Email
from unicodedata import normalize
from flask_login import UserMixin, login_user, current_user


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    """Represents a user, includes extensive validation at initialisation."""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    validated_username = String(minsize=1, maxsize=64)
    validated_email = Email()

    def __init__(self, username, email, password):
        """ Initialises and validates new user.
        Checks if
            1) user is already logged in
            2) parameters are valid
            3) username or email is already in database
        and normalises the username string and sets the password as a hash.
        """

        if current_user.is_authenticated:
            raise RegistrationError("Already authenticated.")

        try:
            self.username = self.validated_username = normalize('NFC', username)
            self.email = self.validated_email = email
            self.set_password(password)
        except ValueError as e:
            raise RegistrationError(str(e))
        except TypeError:
            raise RegistrationError('''Invalid registration: Must be of format:
                                       "user_name": String,
                                       "password": String
                                    ''')
        if User.query.filter_by(username=self.username).first() is not None:
            raise RegistrationError("Username is already taken.")
        if User.query.filter_by(email=self.email).first() is not None:
            raise RegistrationError("Email is already registered.")

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def register(self):
        """Save the user instance in the database and logs the user in."""
        db.session.add(self)
        db.session.commit()
        login_user(self)


class Login:
    """Logs-in a registered user."""
    username = String(minsize=1, maxsize=64)

    def __init__(self, username, password):
        """Login object
            1) validates login payload
            2) checks if user exists
            3) validates password
        """
        try:
            self.username = normalize('NFC', username)
            self.password = password
        except (TypeError, ValueError):
            raise LoginError('''Invalid data. Must be of format:
                                username: string,
                                password: string
                            ''')
        self.authenticate()

    def authenticate(self):
        """Helper functions that queries the database for the user and checks the password."""
        user = User.query.filter_by(username=self.username).first()
        if user is None or not user.check_password(self.password):
            raise LoginError('User is not registered.')
        load_user(user)