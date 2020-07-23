from flask import request, jsonify
from api_app.validation import RegistrationError, LoginError, PayloadError
from api_app.models import User, Login
from api_app.questionnaire import Questionnaire
from flask_login import current_user, logout_user, login_required


def register_routes(app):
    @app.route('/')
    def hello_world():
        return 'Hello World! Please use a http-client like Postman or Insomnia to talk to the API.'

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Register and login new user."""
        try:
            user = User(**(request.json or {}))
            user.register()
        except (PayloadError, RegistrationError) as e:
            return e.json, 422
        return 'Successfully registered and logged in.', 200

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Login existing user."""
        if current_user.is_authenticated:
            return 'Already logged in.', 200
        try:
            Login(**(request.json or {}))
        except (PayloadError, LoginError) as e:
            return e.json, 422
        return 'Successfully logged in.', 200

    @app.route('/logout')
    def logout():
        """Logout any user."""
        logout_user()
        return jsonify('Logged out.'), 200

    @app.route('/recommendation', methods=['POST'])
    @login_required
    def recommendation_route():
        """Returns a insurance recommendation for the posted data."""
        try:
            questionnaire = Questionnaire(**(request.json or {}))
        except PayloadError as e:
            return e.json, 422
        return questionnaire.recommendation(), 200

    return app
