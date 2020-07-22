from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, logout_user
from questionnaire import Questionnaire
from validation import RegistrationError, LoginError
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
    """Registers and logs-in a new user."""
    try:
        user = User(**request.json)
        user.register()
    except ValueError as e:
        return str(e), 422
    except TypeError:
        return '''Invalid registration: Must be of format:
                    "user_name": String
                    "password": String
                ''', 422
    except RegistrationError as e:
        return str(e), 422
    return 'Successfully registered and logged in', 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return 'Already logged in.', 200
    try:
        User.login(**request.json)
    except (TypeError, ValueError):
        return '''Invalid data. Must be of format:
                    username: string,
                    password: string
                ''', 422
    except LoginError as e:
        return 'User is not registered.', 422
    return 'Successfully logged in.', 200


@app.route('/logout')
def logout():
    logout_user()
    return 'Logged out.', 200


@app.route('/recommendation', methods=['POST'])
def recommendation_route():
    """Returns a insurance recommendation for the posted data."""
    try:
        questionnaire = Questionnaire(**request.json)
    except ValueError as e:
        return str(e), 422
    except TypeError as e:
        print(e)
        return '''Invalid data. Must be of format:
                  "first_name": String,
                  "address": String,
                  "occupation": String(OneOf('Employed', 'Student', 'Self-Employed')),
                  "email_address": String,
                  "children": Boolean,
                  "num_children": Optional(int)
                ''', 422
    return questionnaire.recommendation(), 200


if __name__ == '__main__':
    app.run()
