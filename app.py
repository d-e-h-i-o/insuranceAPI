from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, logout_user
from questionnaire import Questionnaire
from validation import RegistrationError, LoginError, PayloadError
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from models import User


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register and login new user."""
    try:
        user = User(**request.json)
        user.register()
    except (PayloadError, RegistrationError) as e:
        return str(e), 422
    return 'Successfully registered and logged in.', 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login existing user."""
    if current_user.is_authenticated:
        return 'Already logged in.', 200
    try:
        User.login(**request.json)
    except (PayloadError, LoginError) as e:
        return str(e), 422
    return 'Successfully logged in.', 200


@app.route('/logout')
def logout():
    """Logout any user."""
    logout_user()
    return 'Logged out.', 200


@app.route('/recommendation', methods=['POST'])
def recommendation_route():
    """Returns a insurance recommendation for the posted data."""
    try:
        questionnaire = Questionnaire(**request.json)
    except PayloadError as e:
        return str(e), 422
    return questionnaire.recommendation(), 200


if __name__ == '__main__':
    app.run()
